from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models


class NetworkOperator(models.Model):
    name = models.CharField(_('Operator\'s name'), max_length=255, null=False)
    network_code = models.PositiveSmallIntegerField(null=False)

    class Meta:
        verbose_name = _('Network operator')
        verbose_name_plural = _('Network operators')


class Measurement(models.Model):
    operator = models.ForeignKey(
        NetworkOperator,
        models.CASCADE,
        related_name='measurement',
    )
    coverage_2G = models.BooleanField(default=False)
    coverage_3G = models.BooleanField(default=False)
    coverage_4G = models.BooleanField(default=False)
    geometry = models.PointField(srid=4326)
