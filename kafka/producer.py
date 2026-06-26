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

# Read dataset
df = pd.read_csv("data/UNSW_NB15_training-set.csv")

# Remove unwanted columns
df = df.drop(columns=["label", "attack_cat"], errors="ignore")

print("Starting dataset stream...")

# Send only the first 50 records
for count, (_, row) in enumerate(df.head(50).iterrows(), start=1):
    producer.send(
        "network_logs",
        row.to_dict()
    )

    print(f"Sent record #{count}")
    time.sleep(0.5)

producer.flush()

print("Successfully sent 50 records.")