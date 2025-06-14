import csv
import os
from collections import deque

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def dashboard(request):
    """Main dashboard view"""
    return render(request, "signals/dashboard.html")


def sensor_data_api(request):
    """API endpoint to get latest sensor data"""
    n_rows = 100

    try:
        csv_path = settings.CSV_FILE_PATH

        if not os.path.exists(csv_path):
            return JsonResponse(
                {"error": "CSV file not found", "data": [], "latest": {}}
            )

        data = []
        latest_data = {}

        with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
            sample = deque(csvfile, maxlen=n_rows)
            sample = "".join(sample)
            csvfile.seek(0)

            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)
            has_header = sniffer.has_header(sample)

            reader = csv.reader(csvfile, dialect)

            if has_header:
                headers = next(reader)

            rows = list(reader)
            recent_rows = rows[-n_rows:] if len(rows) > n_rows else rows

            for i, row in enumerate(recent_rows):
                if len(row) >= 9:
                    try:
                        latitude_val = float(row[0])
                        longitude_val = float(row[1])
                        positionX_val = float(row[2])
                        positionY_val = float(row[3])
                        velocityX_val = float(row[4])
                        velocityY_val = float(row[5])
                        accelerationX_val = float(row[6])
                        accelerationY_val = float(row[7])
                        timestamp_str = row[8]

                        # ➕ Opcional: padroniza o formato do timestamp
                        # Exemplo: se vier no formato "01/06/2025 15:23", converte:
                        # timestamp_val = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M").isoformat()
                        timestamp_val = timestamp_str

                        data.append(
                            {
                                "index": i,
                                "latitude": latitude_val,
                                "longitude": longitude_val,
                                "timestamp": timestamp_val,
                                "positionX": positionX_val,
                                "positionY": positionY_val,
                                "velocityX": velocityX_val,
                                "velocityY": velocityY_val,
                                "accelerationX": accelerationX_val,
                                "accelerationY": accelerationY_val,
                            }
                        )

                        latest_data = {
                            "latitude": latitude_val,
                            "longitude": longitude_val,
                            "timestamp": timestamp_val,
                            "positionX": positionX_val,
                            "positionY": positionY_val,
                            "velocityX": velocityX_val,
                            "velocityY": velocityY_val,
                            "accelerationX": accelerationX_val,
                            "accelerationY": accelerationY_val,
                        }
                    except (ValueError, IndexError):
                        continue

        return JsonResponse(
            {
                "data": data,
                "latest": latest_data,
                "total_rows": len(rows),
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e), "data": [], "latest": {}})
