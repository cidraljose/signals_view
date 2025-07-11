from django.urls import path

from .views import get_logs, send_udp_message, udp_config_view

urlpatterns = [
    path("", udp_config_view, name="udp_config"),
    path("logs/", get_logs, name="udp_logs"),
    path("udp/send_message/", send_udp_message, name="send_udp_message"),
]
