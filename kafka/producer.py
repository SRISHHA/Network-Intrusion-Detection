import pandas as pd
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka-network2026-srishha2001-bd1.i.aivencloud.com:25963",
    security_protocol="SSL",
    ssl_cafile="certs/ca.pem",
    ssl_certfile="certs/service.cert",
    ssl_keyfile="certs/service.key",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv("data/UNSW_NB15_training-set.csv")

df = df.drop(
    columns=["label", "attack_cat"],
    errors="ignore"
)

count = 0

while True:

    print("Starting dataset stream...")

    for _, row in df.iterrows():

        producer.send(
            "network_logs",
            row.to_dict()
        )

        count += 1

        print(f"Sent record #{count}")

        time.sleep(0.5)

    producer.flush()

    print("Dataset completed. Restarting...")