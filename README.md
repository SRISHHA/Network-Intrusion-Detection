# Network-Intrusion-Detection
# 🚀 Real-Time Network Intrusion Detection System using Machine Learning & Apache Kafka

## 📌 Overview

This project implements an **end-to-end Real-Time Network Intrusion Detection System (NIDS)** that combines Machine Learning with event streaming using **Apache Kafka**. The system is capable of identifying whether incoming network traffic is **Normal** or **Malicious**, and if malicious, it further classifies the attack into its corresponding attack category.

Unlike traditional offline ML projects, this solution simulates a real-world streaming environment where network packets are continuously processed, analyzed, and visualized through an interactive dashboard.

---

# 🎯 Objectives

* Detect malicious network traffic in real time.
* Perform binary classification (Normal vs Attack).
* Perform multi-class attack classification.
* Compare multiple machine learning algorithms.
* Deploy trained models for real-time inference.
* Stream network packets using Apache Kafka.
* Visualize intrusion statistics through a live dashboard.

---

# 📂 Dataset

The project uses the **UNSW-NB15 Network Intrusion Detection Dataset**, which contains modern network traffic with both benign and malicious connections.

The dataset contains multiple attack categories including:

* Generic
* Exploits
* DoS
* Reconnaissance
* Fuzzers
* Shellcode
* Worms
* Backdoor
* Analysis

---

# 🛠️ Project Workflow

## 1. Data Preprocessing

The raw dataset was cleaned and transformed before model training.

Performed operations include:

* Missing value handling
* Feature encoding
* Feature scaling
* Target encoding
* Train/Test split
* Data preprocessing pipeline creation

---

## 2. Model Development

Three supervised machine learning algorithms were trained and evaluated:

* Decision Tree
* Random Forest
* XGBoost

The models were evaluated for two different prediction tasks:

### Binary Classification

Predict whether the network traffic is:

* Normal
* Attack

### Multi-Class Classification

If traffic is malicious, identify the exact attack category.

Example attack classes:

* Generic
* Exploits
* DoS
* Shellcode
* Backdoor
* Fuzzers
* Reconnaissance
* Analysis
* Worms

---

# 📊 Model Comparison

All three models were compared using standard evaluation metrics.

| Model         | Binary Classification | Multi-Class Classification |
| ------------- | --------------------- | -------------------------- |
| Decision Tree | Evaluated             | Evaluated                  |
| Random Forest | Evaluated             | Evaluated                  |
| XGBoost       | ⭐ Best                | ⭐ Best                     |

XGBoost achieved the best overall performance for both binary and multi-class intrusion detection.

---

# ⚖️ Handling Class Imbalance

The multi-class dataset contained significant class imbalance.

Different strategies were explored:

* SMOTE oversampling
* Class-weighted learning

Although SMOTE was initially experimented with, **class-weighted learning produced better generalization**, especially for minority attack categories while maintaining overall model performance.

Therefore, weighted training was used in the final implementation.

---

# 💾 Model Serialization

The trained artifacts were exported using Pickle for deployment.

Saved artifacts include:

* Binary Classification Model
* Multi-Class Classification Model
* Binary Feature Scaler
* Multi-Class Feature Scaler
* Feature Encoders
* Target Label Encoder

These serialized models are used directly during real-time inference.

---

# ⚡ Real-Time Streaming Pipeline

The project simulates a real-world intrusion detection pipeline using Apache Kafka.

## Producer

* Reads network traffic records
* Streams packets continuously to Kafka Topic

## Consumer

For every incoming packet:

1. Receives message from Kafka
2. Applies feature encoding
3. Performs feature scaling
4. Runs Binary Classification
5. If attack is detected:

   * Performs Multi-Class Classification
6. Stores predictions into a CSV log

This creates a complete real-time prediction pipeline.

---

# ☁️ Kafka Deployment

Apache Kafka was hosted using a cloud-based Kafka service (Event Cloud) to simulate distributed real-time message streaming.

The streaming architecture separates data producers and consumers similar to modern event-driven systems used in production.

---

# 📈 Dashboard

A Gradio dashboard was developed to monitor the system.

The dashboard provides:

* Latest prediction records
* Packet ID
* Timestamp
* Binary prediction
* Attack category
* Total processed packets
* Attack distribution
* Live attack count table
* Attack frequency visualization
* Refresh option for latest predictions

This enables real-time monitoring of detected network intrusions.

---

# 🏗️ System Architecture

                UNSW-NB15 Dataset
                        │
                        ▼
             Data Cleaning & Preprocessing
                        │
                        ▼
               Feature Engineering
                        │
                        ▼
     Decision Tree | Random Forest | XGBoost
                        │
          Model Evaluation & Comparison
                        │
              Best Model (XGBoost)
                        │
        Save Models + Scalers + Encoders
                        │
                        ▼
                  start.py
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
  Producer.py     Consumer.py      Gradio Dashboard
        │               │                ▲
        │               ▼                │
        └────────► Kafka Topic ──────────┘
                        │
                        ▼
          Encoding → Scaling → Prediction
                        │
        Binary → Multi-Class (if Attack)
                        │
                        ▼
               Prediction CSV Log
                        │
                        ▼
               Live Dashboard Updates

---

# 💻 Tech Stack

**Programming**

* Python

**Machine Learning**

* Scikit-learn
* XGBoost

**Data Processing**

* Pandas
* NumPy

**Model Serialization**

* Pickle

**Streaming**

* Apache Kafka

**Cloud**

* Event Cloud Kafka

**Visualization**

* Gradio

---
🚀 Automated Project Launcher

To simplify project execution, a start.py script was developed that automatically orchestrates all project components.

Instead of manually launching multiple processes, executing a single command initializes the complete intrusion detection pipeline.

start.py automatically:
Starts the Kafka Consumer
Starts the Kafka Producer
Launches the Gradio Dashboard
Establishes the complete real-time prediction pipeline
Enables immediate monitoring of streamed network traffic through a single entry point

This automation improves usability and simulates the startup behavior of a production-ready application, allowing users to run the entire system with a single command.


# 🚀 Key Features

* End-to-end Network Intrusion Detection System
* Binary and Multi-Class Attack Detection
* Model comparison across multiple algorithms
* XGBoost-based production inference
* Class imbalance handling using weighted learning
* Kafka-based real-time streaming pipeline
* Automated preprocessing before inference
* Live monitoring dashboard using Gradio
* Modular Producer-Consumer architecture
* Real-time prediction logging
* Single-command project execution using `start.py`
* Automated orchestration of Producer, Consumer, and Dashboard
* End-to-end real-time streaming and prediction workflow

---

# Future Improvements

* Deploy using Docker containers
* Kubernetes orchestration
* Real-time database integration
* REST API using FastAPI
* Grafana monitoring
* Model retraining pipeline
* CI/CD deployment
* Explainable AI using SHAP

---

# Conclusion

This project demonstrates how Machine Learning can be integrated with real-time event streaming to build an intelligent Network Intrusion Detection System. By combining XGBoost, Apache Kafka, cloud-hosted streaming infrastructure, and an interactive Gradio dashboard, the solution provides a practical simulation of a production-grade cybersecurity monitoring pipeline.
