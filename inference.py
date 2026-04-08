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
    reset_url = f"{API_BASE_URL}/reset"
    try:
        obs_resp = requests.post(reset_url)
        if obs_resp.status_code != 200:
            print(f"Reset failed! URL: {reset_url}, Status: {obs_resp.status_code}, Response: {obs_resp.text}")
            return  # Exit gracefully instead of raising
        
        obs = obs_resp.json()
    except Exception as e:
        print(f"Exception during reset: {e}")
        return

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

        try:
            step_resp = requests.post(f"{API_BASE_URL}/step", json=action)
            if step_resp.status_code != 200:
                print(f"Step failed! Status: {step_resp.status_code}, Response: {step_resp.text}")
                return
            result = step_resp.json()
        except Exception as e:
            print(f"Exception during step: {e}")
            return

        obs = result.get("observation", {})
        total_score += result.get("reward", {}).get("score", 0)
        done = result.get("done", False)

    print("Final Score:", total_score)


if __name__ == "__main__":
    run()