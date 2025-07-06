import os
import subprocess
import openai

def get_recent_logs():
    # Grep for CPU-related logs and return last 100 matches
    result = subprocess.run(
        "grep -i 'cpu\\|usage\\|load' /var/log/syslog | tail -n 100",
        shell=True,
        stdout=subprocess.PIPE
    )
    return result.stdout.decode('utf-8')

def analyze_logs_with_llm(log_data):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise Exception("OpenAI API key not set in environment variable 'OPENAI_API_KEY'.")

    prompt = f"""
You are a DevOps assistant. The system may have experienced high CPU usage.

Analyze the following logs and respond with one of:
- A brief summary if high CPU usage is present and a root cause is evident.
- Or say "No CPU issue detected in logs" if there are no signs.

Logs:
{log_data}
"""


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    logs = get_recent_logs()
    result = analyze_logs_with_llm(logs)
    print("LLM Analysis Result:")
    print(result)

