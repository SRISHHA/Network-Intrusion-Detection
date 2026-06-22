from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "network_logs",

    bootstrap_servers=
    "kafka-network2026-srishha2001-bd1.i.aivencloud.com:25963",

    security_protocol="SSL",

    ssl_cafile="certs/ca.pem",
    ssl_certfile="certs/service.cert",
    ssl_keyfile="certs/service.key",

    value_deserializer=lambda m:
    json.loads(m.decode("utf-8"))
)

print("Waiting...")

for msg in consumer:
    print(msg.value)
