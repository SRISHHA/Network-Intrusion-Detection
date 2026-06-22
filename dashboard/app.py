import pandas as pd
import gradio as gr
import os

CSV_FILE = "logs/predictions.csv"

def load_data():

    if not os.path.exists(CSV_FILE):
        return 0, 0, pd.DataFrame(), pd.DataFrame()

    df = pd.read_csv(CSV_FILE)

    total_packets = len(df)

    total_attacks = len(
        df[df["prediction"] == "Attack"]
    )

    attack_counts = (
        df["attack_type"]
        .value_counts()
        .reset_index()
    )

    attack_counts.columns = [
        "Attack Type",
        "Count"
    ]

    recent = df.tail(20)

    return (
        total_packets,
        total_attacks,
        attack_counts,
        recent
    )


with gr.Blocks() as demo:

    gr.Markdown("# 🚨 Real-Time Intrusion Detection Dashboard")

    refresh_btn = gr.Button("Refresh")

    total_packets = gr.Number(label="Total Packets")
    total_attacks = gr.Number(label="Total Attacks")

    attack_table = gr.Dataframe(
        label="Attack Distribution"
    )

    recent_table = gr.Dataframe(
        label="Recent Predictions"
    )

    refresh_btn.click(
        fn=load_data,
        outputs=[
            total_packets,
            total_attacks,
            attack_table,
            recent_table
        ]
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)