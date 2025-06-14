from django import forms
from django.http import JsonResponse
from django.shortcuts import render

from .udp_listener import UDPServer, logs

# Global instance to control the server
udp_server_instance = None


class UDPConfigForm(forms.Form):
    host = forms.CharField(initial="0.0.0.0")
    port = forms.IntegerField(initial=6666)


def udp_config_view(request):
    global udp_server_instance
    message = ""

    if request.method == "POST":
        form = UDPConfigForm(request.POST)
        if form.is_valid():
            host = form.cleaned_data["host"]
            port = form.cleaned_data["port"]

            if "start" in request.POST:
                if udp_server_instance and udp_server_instance.is_alive():
                    message = "Server is already running."
                else:
                    udp_server_instance = UDPServer(host, port)
                    udp_server_instance.start()
                    message = f"Server started on {host}:{port}"

            elif "stop" in request.POST:
                if udp_server_instance and udp_server_instance.is_alive():
                    udp_server_instance.stop()
                    udp_server_instance = None
                    message = "Server stopped."
                else:
                    message = "Server is not running."

    else:
        form = UDPConfigForm()

    server_status = (
        "Running"
        if udp_server_instance and udp_server_instance.is_alive()
        else "Stopped"
    )

    return render(
        request,
        "udp_server/udp_config.html",
        {
            "form": form,
            "message": message,
            "server_status": server_status,
        },
    )


def get_logs(request):
    return JsonResponse({"logs": logs})
