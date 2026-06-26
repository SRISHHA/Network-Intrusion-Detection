import subprocess
import time

# Start Producer
producer = subprocess.Popen(["python", "kafka/producer.py"])

# Give producer time to connect to Kafka
time.sleep(2)

# Start Consumer
consumer = subprocess.Popen(["python", "kafka/consumer.py"])

# Give consumer time to initialize
time.sleep(2)

# Start Dashboard
dashboard = subprocess.Popen(["python", "dashboard/app.py"])

# Wait for all processes
producer.wait()
consumer.wait()
dashboard.wait()
