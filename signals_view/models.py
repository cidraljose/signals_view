from django.db import models


class CSVData(models.Model):
    """
    Modelo para os dados lidos no arquivo CSV.
    Os campos correspondem aos dados esperados do ESP32.
    """

    anguloZ = models.IntegerField(null=True, blank=True, verbose_name="anguloZ")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    latitude = models.FloatField(null=True, blank=True, verbose_name="latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="longitude")
    position = models.FloatField(null=True, blank=True, verbose_name="position")
    # positionX = models.FloatField(null=True, blank=True, verbose_name="positionX")
    # positionY = models.FloatField(null=True, blank=True, verbose_name="positionY")
    velocity = models.FloatField(null=True, blank=True, verbose_name="velocity")
    # velocityX = models.FloatField(null=True, blank=True, verbose_name="velocityX")
    # velocityY = models.FloatField(null=True, blank=True, verbose_name="velocityY")
    acceleration = models.FloatField(null=True, blank=True, verbose_name="acceleration")
    # accelerationX = models.FloatField(
    #     null=True, blank=True, verbose_name="accelerationX"
    # )
    # accelerationY = models.FloatField(
    #     null=True, blank=True, verbose_name="accelerationY"
    # )
