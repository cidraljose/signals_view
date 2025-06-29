import csv
import socket
import threading
from datetime import datetime

from django.conf import settings

MAX_LOGS = 15

logs = []


class UDPServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.sock = None

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()

    def run(self):
        global logs
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        logs.append(f"Listening on {self.host}:{self.port}")

        with open(settings.CSV_FILE_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "latitude",
                    "longitude",
                    "position",
                    # "positionX",
                    # "positionY",
                    "velocity",
                    # "velocityX",
                    # "velocityY",
                    "acceleration",
                    "angulo",
                    # "accelerationX",
                    # "accelerationY",
                    "timestamp",
                ]
            )

        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode("utf-8").strip()
                logs.append(f"From {addr}: {message}, [{datetime.now().isoformat()}]")

                # Verifica se ultrapassou o limite
                if len(logs) >= MAX_LOGS:
                    logs.pop(0)

                # Grava com timestamp no CSV
                row = message.split(",") + [datetime.now().isoformat()]
                print(row)
                with open(settings.CSV_FILE_PATH, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(row)

            except Exception as e:
                if self.running:
                    logs.append(f"Error: {e}")
                break

        logs.append("UDP server stopped")
