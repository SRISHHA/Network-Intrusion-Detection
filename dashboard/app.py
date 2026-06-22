import os
import glob
import pandas as pd
import gradio as gr
import plotly.express as px


def get_latest_csv():

    files = glob.glob("logs/*.csv")

    if not files:
        return None

    return max(files, key=os.path.getctime)


def load_data():

    csv_file = get_latest_csv()

    if csv_file is None:

        return (
            "No file",
            0,
            0,
            pd.DataFrame(),
            pd.DataFrame()
        )

    df = pd.read_csv(csv_file)

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
        os.path.basename(csv_file),
        total_packets,
        total_attacks,
        attack_counts,
        recent
    )
import plotly.express as px


def attack_chart():

    csv_file = get_latest_csv()

    if csv_file is None:
        return None

    df = pd.read_csv(csv_file)

    counts = (
        df["attack_type"]
        .value_counts()
        .reset_index()
    )

    counts.columns = [
        "Type",
        "Count"
    ]

    fig = px.bar(
        counts,
        x="Type",
        y="Count",
        title="Network Traffic Classification",
        text="Count"
    )

    fig.update_layout(
        xaxis_title="Traffic Type",
        yaxis_title="Count",
        height=450
    )

    return fig


with gr.Blocks() as demo:

    gr.Markdown(
        "# 🚨 Network Intrusion Detection Dashboard"
    )

    refresh_btn = gr.Button("Refresh")

    current_file = gr.Textbox(
        label="Current Log File"
    )

    total_packets = gr.Number(
        label="Total Packets"
    )

    total_attacks = gr.Number(
        label="Total Attacks"
    )

    attack_table = gr.Dataframe(
        label="Attack Distribution"
    )

    attack_plot = gr.Plot(
        label=" "
    )

    recent_table = gr.Dataframe(
        label="Recent Predictions"
    )

    

    

    refresh_btn.click(
        fn=load_data,
        outputs=[
            current_file,
            total_packets,
            total_attacks,
            attack_table,
            recent_table
        ]
    )

    refresh_btn.click(
    fn=attack_chart,
    outputs=attack_plot

    )

    demo.load(
        fn=load_data,
        outputs=[
            current_file,
            total_packets,
            total_attacks,
            attack_table,
            recent_table
        ]
    )

    demo.load(
        fn=attack_chart,
        outputs=attack_plot
    )

demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)