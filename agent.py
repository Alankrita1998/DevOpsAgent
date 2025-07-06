import subprocess
import analyze_logs
import email_notify

def main():
    logs = analyze_logs.get_recent_logs()
    analysis = analyze_logs.analyze_logs_with_llm(logs)

    print("LLM Analysis Result:")
    print(analysis)

    if "high cpu" in analysis.lower() or "cpu usage" in analysis.lower():
        print("Triggering remediation...")
        subprocess.run(["sudo", "python3", "remediate.py"])
        email_notify.send_email(
            "CPU Spike Detected",
            f"High CPU usage found.\n\nLLM Analysis:\n{analysis}\n\nRemediation attempted."
        )
    else:
        email_notify.send_email(
            "System Stable",
            f"No CPU issue detected.\n\nLLM Analysis:\n{analysis}"
        )

if __name__ == "__main__":
    main()
