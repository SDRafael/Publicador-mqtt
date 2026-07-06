import json
import os
import random
import socket
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mosquitto")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "lab/telemetria/estacao01")
PUBLISH_INTERVAL = float(os.getenv("PUBLISH_INTERVAL", "5"))
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", f"publisher-{socket.gethostname()}")


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[publisher] conectado ao broker com reason_code={reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"[publisher] desconectado. reason_code={reason_code}")


def build_payload(sequence: int) -> str:
    payload = {
        "host": "servidor01",
        "latencia_ms": random.randint(5, 40),
        "throughput_mbps": random.randint(100, 300),
        "uso_cpu": random.randint(10, 95),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return json.dumps(payload)


def connect_with_retry(client: mqtt.Client) -> None:
    while True:
        try:
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            return
        except Exception as exc:
            print(f"[publisher] falha ao conectar: {exc}. Tentando novamente em 2s...")
            time.sleep(2)


def main() -> None:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
        protocol=mqtt.MQTTv311,
        clean_session=True,
    )

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    connect_with_retry(client)
    client.loop_start()

    sequence = 1
    try:
        while True:
            payload = build_payload(sequence)
            info = client.publish(TOPIC, payload=payload, qos=0, retain=True)
            info.wait_for_publish()

            print(f"[publisher] tópico={TOPIC} payload={payload}")
            sequence += 1
            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        print("[publisher] encerrando...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()