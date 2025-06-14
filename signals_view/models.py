from django.db import models


class CSVData(models.Model):
    """
    Modelo para os dados lidos no arquivo CSV.
    Os campos correspondem aos dados esperados do ESP32.
    """

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    latitude = models.FloatField(null=True, blank=True, verbose_name="latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="longitude")
    positionX = models.FloatField(null=True, blank=True, verbose_name="positionX")
    positionY = models.FloatField(null=True, blank=True, verbose_name="positionY")
    velocityX = models.FloatField(null=True, blank=True, verbose_name="velocityX")
    velocityY = models.FloatField(null=True, blank=True, verbose_name="velocityY")
    accelerationX = models.FloatField(
        null=True, blank=True, verbose_name="accelerationX"
    )
    accelerationY = models.FloatField(
        null=True, blank=True, verbose_name="accelerationY"
    )
