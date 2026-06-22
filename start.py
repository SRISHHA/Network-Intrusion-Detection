import subprocess
import time

consumer = subprocess.Popen(
    ["python", "kafka/consumer.py"]
)

time.sleep(5)

dashboard = subprocess.Popen(
    ["python", "dashboard/app.py"]
)

consumer.wait()
dashboard.wait()