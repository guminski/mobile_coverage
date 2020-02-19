from django.core.management.base import BaseCommand
import csv
from search_api.models import NetworkOperator, Measurement
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = "Loads data from CSV file to db"

    OPERATOR_NAMES = {
        20801: 'Orange',
        20810: 'SFR',
        20815: 'Free',
        20820: 'Bouygue',
    }

    def handle(self, *args, **options):
        network_codes = set()

        with open('mobiles_france.csv') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                network_codes.add(int(row['Operateur']))

        operators = dict()
        for code in network_codes:
            obj, created = NetworkOperator.objects.get_or_create(
                network_code=code,
                name=self.OPERATOR_NAMES.get(code, '')
            )
            operators[code] = obj

        with open('mobiles_france.csv') as f:
            reader = csv.DictReader(f, delimiter=';')
            to_create = []
            for row in reader:
                x = int(row['X'])
                y = int(row['Y'])
                point = Point(x=x, y=y, srid=2154)
                to_create.append(
                    Measurement(
                        geometry=point,
                        operator=operators[int(row['Operateur'])],
                        coverage_2G=True if row['2G'] == '1' else False,
                        coverage_3G=True if row['3G'] == '1' else False,
                        coverage_4G=True if row['4G'] == '1' else False,
                    ))
            Measurement.objects.bulk_create(to_create, batch_size=2000)
            self.stdout.write(self.style.SUCCESS(f'--- Loading data finished ---'))
