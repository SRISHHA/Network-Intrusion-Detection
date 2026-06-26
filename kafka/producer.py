import json
import time
import pandas as pd

from kafka import KafkaProducer

# ==================================
# Kafka Producer
# ==================================

producer = KafkaProducer(
    bootstrap_servers="kafka-network2026-srishha2001-bd1.i.aivencloud.com:25963",
    security_protocol="SSL",
    ssl_cafile="certs/ca.pem",
    ssl_certfile="certs/service.cert",
    ssl_keyfile="certs/service.key",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

# ==================================
# Load Dataset
# ==================================

DATASET_PATH = "data/UNSW_NB15_training-set.csv"

df = pd.read_csv(DATASET_PATH)

# Remove labels (used only during training)
df = df.drop(
    columns=["label", "attack_cat"],
    errors="ignore"
)

print(f"Loaded {len(df)} records.")
print("Starting dataset stream...\n")

# ==================================
# Stream Dataset to Kafka
# ==================================

TOTAL_RECORDS = 50
DELAY = 0.7  # seconds

for index, row in df.head(TOTAL_RECORDS).iterrows():

    # Convert row to dictionary
    message = row.to_dict()

    # Add unique record ID
    message["id"] = index + 1

    producer.send(
        "network_logs",
        value=message
    )

    print(f"Sent Record ID: {message['id']}")

    time.sleep(DELAY)

# ==================================
# Finish
# ==================================

producer.flush()
producer.close()

print(f"\nSuccessfully streamed {TOTAL_RECORDS} records.")