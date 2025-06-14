from django.urls import path

from .views import get_logs, udp_config_view

urlpatterns = [
    path("", udp_config_view, name="udp_config"),
    path("logs/", get_logs, name="udp_logs"),
]
