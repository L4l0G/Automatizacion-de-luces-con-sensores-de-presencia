#!/usr/bin/env python3
import time, json, random
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

BROKER = "100.101.98.30"
PORT = 1883
TOPIC = "home/office/pir1"
CLIENT_ID = "pir-sim-01"
PUBLISH_INTERVAL = 2.0  # segundos entre mensajes (ajusta a tu necesidad)

client = mqtt.Client(CLIENT_ID)
client.connect(BROKER, PORT)

def simulate_pir():
    # Simula ráfagas: mayor probabilidad de no detección, pequeñas ráfagas de detección
    if random.random() < 0.08:  # 8% prob de iniciar una ráfaga de movimiento
        # ráfaga de 1-6 mensajes con motion=true
        for _ in range(random.randint(1,6)):
            yield True
        # después vuelve a false
        yield False
    else:
        yield False

try:
    while True:
        motion = next(simulate_pir())
        payload = {
            "sensor_id": "pir1",
            "motion": bool(motion),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        client.publish(TOPIC, json.dumps(payload), qos=0)
        print("Publicado:", payload)
        time.sleep(PUBLISH_INTERVAL)
except KeyboardInterrupt:
    client.disconnect()
    print("Simulador detenido")
