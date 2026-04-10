"""
Inference Script for Customer Support Environment
Uses OpenAI API for decision making with structured output for validator
"""

import os
import sys
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from server.environment import MyEnvironment
from pydantic import BaseModel

# Force flush stdout immediately
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

# Required environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")

class Action(BaseModel):
    action_type: str
    content: str | None = None

class CustomerSupportAgent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
        self.env = MyEnvironment()
    
    def get_llm_action(self, observation, difficulty, step):
        prompt = f"""
You are a customer support agent. Current ticket:
Message: {observation['message']}
Difficulty: {difficulty}
Step: {step}

Choose an action:
- action_type: "technical", "billing", or "escalate"
- content: your response (optional)

Respond with JSON only: {{"action_type": "technical", "content": "Please reset your password"}}
"""
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=100
            )
            response_text = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"action_type": "technical", "content": "Checking your issue"}
        except Exception as e:
            print(f"LLM error: {e}", file=sys.stderr)
            return {"action_type": "technical", "content": "Checking your issue"}
    
    def run_task(self, difficulty):
        # [START] block - Required by validator
        print(f"[START] task={difficulty}", flush=True)
        
        observation = self.env.reset(difficulty)
        total_reward = 0.0
        step = 0
        done = False
        step_rewards = []
        
        while not done and step < 5:
            action_dict = self.get_llm_action(observation, difficulty, step + 1)
            action = Action(**action_dict)
            
            observation, reward, done, info = self.env.step(action)
            step_reward = reward["score"]
            total_reward += step_reward
            step += 1
            step_rewards.append(step_reward)
            
            # [STEP] block - Required by validator (every step)
            print(f"[STEP] step={step} reward={step_reward:.3f}", flush=True)
        
        # Calculate final score (normalized to 0-1)
        final_score = total_reward / 3.0  # Max possible reward is 3 (1 per step)
        final_score = max(0.0, min(1.0, final_score))
        
        # [END] block - Required by validator
        print(f"[END] task={difficulty} score={final_score:.3f} steps={step}", flush=True)
        
        return final_score
    
    def run_all_tasks(self):
        scores = {}
        for difficulty in ["easy", "medium", "hard"]:
            scores[difficulty] = self.run_task(difficulty)
        return scores

def main():
    # Print to stderr for debugging (validator ignores stderr)
    print("🚀 Customer Support Environment - Baseline Inference", file=sys.stderr)
    print(f"Model: {MODEL_NAME}", file=sys.stderr)
    print(f"API Base URL: {API_BASE_URL}", file=sys.stderr)
    
    agent = CustomerSupportAgent()
    scores = agent.run_all_tasks()
    
    # Print summary to stderr (not parsed by validator)
    print("\n" + "="*40, file=sys.stderr)
    print("FINAL BASELINE SCORES", file=sys.stderr)
    print("="*40, file=sys.stderr)
    for diff, score in scores.items():
        print(f"{diff.upper()}: {score:.3f}", file=sys.stderr)
    print(f"\nAverage: {sum(scores.values())/3:.3f}", file=sys.stderr)

if __name__ == "__main__":
    main()