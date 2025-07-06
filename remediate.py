import subprocess
import time
import psutil
from datetime import datetime

# The name of the service we want to monitor and possibly restart
SERVICE_NAME = "docker"  

# healthy CPU usage after remediation
CPU_THRESHOLD = 50  # in percent

# Log file to store remediation history
LOG_FILE = "/var/log/remediation.log"

def log_to_file(message):
    """Append a timestamped message to the remediation log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")

def restart_service(service_name):
    """Attempt to restart the given system service."""
    print(f"Restarting service: {service_name}...")
    try:
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
        log_to_file(f"Successfully restarted: {service_name}")
        print(f"Service restarted successfully: {service_name}")
        return True
    except subprocess.CalledProcessError:
        log_to_file(f"Failed to restart: {service_name}")
        print(f"Restart failed: {service_name}")
        return False

def measure_average_cpu(duration_seconds=10):
    """Measure average CPU usage over a given number of seconds."""
    print(f"Monitoring CPU usage for {duration_seconds} seconds...")
    cpu_samples = []
    for _ in range(duration_seconds):
        cpu_samples.append(psutil.cpu_percent(interval=1))
    average_cpu = sum(cpu_samples) / len(cpu_samples)
    print(f"Average CPU after restart: {average_cpu:.2f}%")
    return average_cpu

if __name__ == "__main__":
    print(f"\nStarting remediation for potential high CPU caused by '{SERVICE_NAME}'\n")

    if restart_service(SERVICE_NAME):
        average_cpu = measure_average_cpu()

        if average_cpu < CPU_THRESHOLD:
            log_to_file(f"Remediation successful. CPU now at {average_cpu:.2f}%.")
            print("CPU usage dropped. System is back to normal.\n")
        else:
            log_to_file(f"CPU still high after restart. Average: {average_cpu:.2f}%")
            print("CPU remains high. Further investigation recommended.\n")
    else:
        print("Remediation could not be completed due to service restart failure.\n")

