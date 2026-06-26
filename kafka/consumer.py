import os
import json
import joblib
import pandas as pd

from kafka import KafkaConsumer
from datetime import datetime
from zoneinfo import ZoneInfo

# ==================================
# Load Models
# ==================================

binary_model = joblib.load("models/xgb_binary.pkl")
multi_model = joblib.load("models/xgb_multi.pkl")

binary_scaler = joblib.load("models/binary_scaler.pkl")
multiclass_scaler = joblib.load("models/multiclass_scaler.pkl")

encoders = joblib.load("models/encoders.pkl")
attack_encoder = joblib.load("models/attack_encoder.pkl")

print("Models loaded successfully")

# ==================================
# Feature Order
# ==================================

FEATURE_COLUMNS = [
    'dur', 'proto', 'service', 'state', 'spkts',
    'dpkts', 'sbytes', 'dbytes', 'rate',
    'sttl', 'dttl', 'sload', 'dload',
    'sloss', 'dloss', 'sinpkt', 'dinpkt',
    'sjit', 'djit', 'swin', 'stcpb',
    'dtcpb', 'dwin', 'tcprtt', 'synack',
    'ackdat', 'smean', 'dmean',
    'trans_depth', 'response_body_len',
    'ct_srv_src', 'ct_state_ttl',
    'ct_dst_ltm', 'ct_src_dport_ltm',
    'ct_dst_sport_ltm', 'ct_dst_src_ltm',
    'is_ftp_login', 'ct_ftp_cmd',
    'ct_flw_http_mthd', 'ct_src_ltm',
    'ct_srv_dst', 'is_sm_ips_ports'
]

# ==================================
# Kafka Consumer
# ==================================

consumer = KafkaConsumer(
    "network_logs",
    bootstrap_servers="kafka-network2026-srishha2001-bd1.i.aivencloud.com:25963",
    security_protocol="SSL",
    ssl_cafile="certs/ca.pem",
    ssl_certfile="certs/service.cert",
    ssl_keyfile="certs/service.key",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="network_ids",
    enable_auto_commit=True
)

print("Waiting for messages...")

# ==================================
# Create Log File
# ==================================

os.makedirs("logs", exist_ok=True)

start_time = datetime.now(ZoneInfo("Asia/Kolkata"))

csv_file = (
    f"logs/predictions_"
    f"{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
)

if not os.path.exists(csv_file):

    pd.DataFrame(columns=[
        "id",
        "timestamp",
        "prediction",
        "attack_type"
    ]).to_csv(csv_file, index=False)


# ==================================
# Prediction Function
# ==================================

def predict_network_log(data):

    df = pd.DataFrame([data])

    # Encode categorical features
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = encoder.transform(df[col])

    # Arrange feature order
    df = df[FEATURE_COLUMNS]

    # Scale
    X_binary = binary_scaler.transform(df)
    X_multi = multiclass_scaler.transform(df)

    # Binary prediction
    binary_pred = binary_model.predict(X_binary)[0]

    if binary_pred == 0:
        return "Normal", "Normal"

    attack_pred = multi_model.predict(X_multi)[0]

    attack_name = attack_encoder.inverse_transform(
        [attack_pred]
    )[0]

    return "Attack", attack_name


# ==================================
# Consume Messages
# ==================================

for msg in consumer:

    try:

        data = msg.value

        # If producer sends an ID, use it.
        # Otherwise use Kafka offset.
        record_id = data.get("id", msg.offset)

        current_time = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")

        prediction, attack_name = predict_network_log(data)

        print(
            f"[ID: {record_id}] "
            f"[{current_time}] "
            f"{prediction} -> {attack_name}"
        )

        result = pd.DataFrame([{
            "id": record_id,
            "timestamp": current_time,
            "prediction": prediction,
            "attack_type": attack_name
        }])

        result.to_csv(
            csv_file,
            mode="a",
            header=False,
            index=False
        )

    except Exception as e:
        print("ERROR:", e)