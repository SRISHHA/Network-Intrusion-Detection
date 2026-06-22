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

# Remove target columns
df = df.drop(
    columns=["label", "attack_cat"],
    errors="ignore"
)

# Testing only
df = df.head(50)

while True:

    for _, row in df.iterrows():

        producer.send(
            "network_logs",
            row.to_dict()
        )

        producer.flush()

        time.sleep(1)

print("All records sent successfully")

