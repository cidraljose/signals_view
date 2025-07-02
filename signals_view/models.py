from django.db import models


class CSVData(models.Model):
    """
    Modelo para os dados lidos no arquivo CSV.
    Os campos correspondem aos dados esperados do ESP32.
    """

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    latitude = models.FloatField(null=True, blank=True, verbose_name="latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="longitude")
    position = models.FloatField(null=True, blank=True, verbose_name="position")
    velocity = models.FloatField(null=True, blank=True, verbose_name="velocity")
    acceleration = models.FloatField(null=True, blank=True, verbose_name="acceleration")
