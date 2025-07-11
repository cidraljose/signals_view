import json
import socket

from django import forms
from django.http import JsonResponse
from django.shortcuts import render

from .udp_listener import UDPServer, logs

# Global instance to control the server
udp_server_instance = None
MAX_LOGS = 200


class UDPConfigForm(forms.Form):
    host = forms.CharField(initial="0.0.0.0")
    port = forms.IntegerField(initial=6669)


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
        # Try to get existing config if the server is running or from the model
        if udp_server_instance and udp_server_instance.is_alive():
            form = UDPConfigForm(
                initial={
                    "host": udp_server_instance.host,
                    "port": udp_server_instance.port,
                }
            )
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


def send_udp_message(request):
    global udp_server_instance
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message_to_send = data.get("message")

            if not message_to_send:
                return JsonResponse(
                    {"status": "error", "message": "No message provided."}, status=400
                )

            # Get the current host and port from the running server instance
            # or from the latest configuration if the server is stopped but you want to send
            if udp_server_instance and udp_server_instance.is_alive():
                target_host = udp_server_instance.host
                target_port = udp_server_instance.port
            else:
                # If the server is not running, you need to decide where to send the message.
                # For this example, let's assume you'd send it to the last configured address
                # or a default. For now, we'll return an error if the server isn't active.
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "UDP server is not running to send messages to.",
                    },
                    status=400,
                )

            # Create a temporary UDP socket to send the message
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender_sock:
                sender_sock.sendto(
                    message_to_send.encode("utf-8"), (target_host, target_port)
                )
                # Add to logs that a message was sent *from* the web interface
                logs.append(
                    f"Sent from web: {message_to_send} to {target_host}:{target_port}"
                )
                if len(logs) >= MAX_LOGS:
                    logs.pop(0)

            return JsonResponse(
                {"status": "success", "message": "Message sent successfully."}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON."}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"Failed to send message: {e}"},
                status=500,
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Only POST requests are allowed."},
            status=405,
        )
