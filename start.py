import subprocess
import time
import signal

processes = []

try:
    print("Starting Consumer...")
    consumer = subprocess.Popen(["python", "kafka/consumer.py"])
    processes.append(consumer)

    # Give consumer time to connect to Kafka
    time.sleep(8)

    print("Starting Dashboard...")
    dashboard = subprocess.Popen(["python", "dashboard/app.py"])
    processes.append(dashboard)

    # Give dashboard time to initialize
    time.sleep(3)

    print("Starting Producer...")
    producer = subprocess.Popen(["python", "kafka/producer.py"])
    processes.append(producer)

    # Wait until producer finishes
    producer.wait()

    print("Producer finished.")

    # Keep consumer and dashboard running
    consumer.wait()
    dashboard.wait()

except KeyboardInterrupt:
    print("\nStopping all processes...")

finally:
    for p in processes:
        if p.poll() is None:
            p.terminate()

    print("All processes stopped.")