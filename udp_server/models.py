"""
Informacoes de configuracao para a conexao UDP
"""

from django.db import models


class UDPConfig(models.Model):
    host = models.CharField(max_length=100, default="0.0.0.0")
    port = models.IntegerField(default=6666)

    def __str__(self):
        return f"{self.host}:{self.port}"
