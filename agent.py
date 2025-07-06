import subprocess
import analyze_logs
import email_notify

def main():
    logs = analyze_logs.get_recent_logs()
    print("Logs being analyzed:")
    print(logs)

    analysis = analyze_logs.analyze_logs_with_llm(logs)

    print("LLM Analysis Result:")
    print(analysis)

    cpu_keywords = ["high cpu", "cpu usage", "cpu utilization", "cpu bottleneck", "load average", "overloaded"]
    if any(keyword in analysis.lower() for keyword in cpu_keywords):
        print("CPU issue detected! Triggering remediation...")
        try:
            subprocess.run(["sudo", "python3", "remediate.py"], check=True)
            email_notify.send_email(
                "CPU Spike Detected",
                f"High CPU usage detected.\n\nLLM Analysis:\n{analysis}\n\nRemediation attempted."
            )
        except subprocess.CalledProcessError as e:
            print(f"Remediation failed: {e}")
    else:
        print("No CPU issue detected.")
        email_notify.send_email(
            "System Stable",
            f"No CPU issue detected.\n\nLLM Analysis:\n{analysis}"
        )

if __name__ == "__main__":
    main()

