import requests
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from requests.exceptions import ConnectTimeout, ReadTimeout
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import (
    GenericViewSet
)

from .models import Measurement, NetworkOperator

class AddressNotFound(APIException):
    status_code = 400
    default_detail = 'Address not found'
    default_code = 'address_not_found'


class QueryParamRequired(APIException):
    status_code = 400
    default_detail = 'Query parameter ?address= required'
    default_code = 'address_required'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class SearchApiView(GenericViewSet):
    """
    Searching view
    ?address=Paris parameter required
    """
    model = NetworkOperator
    queryset = Measurement.objects.all()
    pagination_class = None

    def get_search_param(self):
        search_string = self.request.query_params.get('address', '')
        if not search_string:
            raise QueryParamRequired
        return search_string

    def get_point_obj(self):
        return Point(self.get_coords_from_address(), srid=2154)

    def get_coords_from_address(self):
        params = {
            'limit': 1,
            'q': self.get_search_param(),
        }

        url = 'https://api-adresse.data.gouv.fr/search/'

        try:
            res = requests.get(url, params, timeout=10)
        except (ConnectTimeout, ReadTimeout):
            raise ServiceUnavailable

        content = res.json().get('features', [])

        if not content:
            raise AddressNotFound

        coords = content[0]['geometry']['coordinates']
        return coords

    def search(self, request):
        point = self.get_point_obj()
        operators = NetworkOperator.objects.all()
        found_measurements = []
        for operator in operators:
            obj = Measurement.objects.select_related('operator').filter(operator=operator).annotate(
                distance=Distance('geometry', point)
            ).order_by('distance').first()
            found_measurements.append(obj)

        res = {
            measurement.operator.name: {
                '2G': measurement.coverage_2G, '3G': measurement.coverage_3G, '4G': measurement.coverage_4G
            } for measurement in found_measurements
        }
        return Response(res, status=status.HTTP_200_OK)
