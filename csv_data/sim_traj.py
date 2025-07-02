import csv
import datetime
import random
import time

# Parâmetros da simulação
lat_inicial = -26.23569029586070
lon_inicial = -48.88468918332882
deslocamento_max = 0.00003  # Pequeno deslocamento para simular movimento

pos_inicial = 0.0
vel = 0.0
acc = 0.0

# Estado atual
lat = lat_inicial
lon = lon_inicial
pos = pos_inicial

# Configuração de velocidade e aceleração máximas
vel_max = 0.5
acc_max = 0.1

# intervalo de tempo
dt = 0.5

# Escreve cabeçalhos no CSV
with open("sensor_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "latitude",
            "longitude",
            "position",
            "velocity",
            "acceleration",
            "timestamp",
        ]
    )

# Simulação contínua
while True:
    # Atualiza latitude e longitude
    lat += random.uniform(-deslocamento_max, deslocamento_max)
    lon += random.uniform(-deslocamento_max, deslocamento_max)

    # Gera aceleração aleatória
    acc = random.uniform(-acc_max, acc_max)

    # Atualiza velocidade com base na aceleração
    vel += acc

    # Limita velocidade
    vel = max(min(vel, vel_max), -vel_max)

    # Atualiza posição
    pos += vel

    # Timestamp
    timestamp = datetime.datetime.now()

    # Dados para gravar
    row = [lat, lon, pos, vel, acc, timestamp]

    # Escreve no CSV
    with open("sensor_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

    # Aguarda próximo ciclo
    time.sleep(dt)
