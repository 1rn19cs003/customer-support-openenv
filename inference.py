import os
import requests
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL")
)

BASE_URL = "http://127.0.0.1:8000"

def run():
    obs = requests.get(f"{BASE_URL}/reset").json()
    total_score = 0

    while True:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[{"role": "user", "content": str(obs)}]
        )

        # Dummy action (baseline)
        action = {
            "action_type": "technical",
            "content": "Please reset your password"
        }

        result = requests.post(f"{BASE_URL}/step", json=action).json()

        total_score += result["reward"]["score"]

        if result["done"]:
            break

    print("Final Score:", total_score)

if __name__ == "__main__":
    run()