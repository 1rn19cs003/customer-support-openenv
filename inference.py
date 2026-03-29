import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Use environment variables (HF Spaces / OpenEnv)
API_BASE_URL = os.getenv("API_BASE_URL") or "http://127.0.0.1:8000"
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

def run():
    # Use POST for reset to satisfy OpenEnv checks
    obs_resp = requests.post(f"{API_BASE_URL}/reset")
    if obs_resp.status_code != 200:
        raise Exception(f"Reset failed: {obs_resp.text}")
    obs = obs_resp.json()
    total_score = 0
    done = False

    while not done:
        message = str(obs).lower()

        # Simple rule-based baseline
        if "refund" in message:
            action = {
                "action_type": "billing",
                "content": "We are checking your refund"
            }
        else:
            action = {
                "action_type": "technical",
                "content": "Please reset your password"
            }

        # POST action to /step
        step_resp = requests.post(f"{API_BASE_URL}/step", json=action)
        if step_resp.status_code != 200:
            raise Exception(f"Step failed: {step_resp.text}")

        result = step_resp.json()
        obs = result.get("observation", {})
        total_score += result.get("reward", {}).get("score", 0)
        done = result.get("done", False)

    print("Final Score:", total_score)


if __name__ == "__main__":
    run()