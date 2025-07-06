from prometheus_api_client import PrometheusConnect
from datetime import datetime, timedelta
import time
import subprocess

# Connect to local Prometheus server 
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

# CPU threshold
THRESHOLD = 80
DURATION = 120

def get_cpu_usage():
    end_time = datetime.now()
    start_time = end_time - timedelta(seconds=30)

    query = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
    result = prom.custom_query(query=query)

    for r in result:
        usage = float(r['value'][1])
        print(f"Current CPU Usage: {usage:.2f}%")
        if usage > THRESHOLD:
            return True, usage
    return False, 0.0

if __name__ == "__main__":
    print("Starting CPU monitor...")
    spike_duration = 0
    while True:
        spike, usage = get_cpu_usage()
        if spike:
            spike_duration += 10
            print(f"CPU Spike Detected: {usage:.2f}%, for {spike_duration} seconds")
        else:
            spike_duration = 0

        if spike_duration >= DURATION:
            print("Sustained spike! Triggering analysis agent...")
            subprocess.run(["python3", "agent.py"])
            break

        time.sleep(10)

