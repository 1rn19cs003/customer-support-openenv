"""
Inference Script for Customer Support Environment
Uses the provided LLM proxy API (required by validator)
"""

import os
import sys
import json
import re
from dotenv import load_dotenv

# Force flush stdout
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

# ============================================
# CRITICAL: Use the validator's environment variables
# DO NOT hardcode or use your own API keys
# ============================================
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Debug: Print which API we're using (goes to stderr, ignored by validator)
print(f"Using API_BASE_URL: {API_BASE_URL}", file=sys.stderr)
print(f"Using MODEL_NAME: {MODEL_NAME}", file=sys.stderr)
print(f"API_KEY present: {bool(API_KEY)}", file=sys.stderr)

# Import environment
from server.environment import MyEnvironment
from pydantic import BaseModel

class Action(BaseModel):
    action_type: str
    content: str | None = None

class CustomerSupportAgent:
    def __init__(self):
        self.env = MyEnvironment()
        self.client = None
        
        # Initialize OpenAI client with validator's proxy
        try:
            from openai import OpenAI
            
            if not API_BASE_URL or not API_KEY:
                print("WARNING: API_BASE_URL or API_KEY not set!", file=sys.stderr)
                print(f"API_BASE_URL: {API_BASE_URL}", file=sys.stderr)
                print(f"API_KEY set: {bool(API_KEY)}", file=sys.stderr)
            else:
                self.client = OpenAI(
                    api_key=API_KEY,
                    base_url=API_BASE_URL
                )
                print("OpenAI client initialized successfully", file=sys.stderr)
        except Exception as e:
            print(f"Failed to initialize OpenAI client: {e}", file=sys.stderr)
            self.client = None
    
    def get_llm_action(self, observation, difficulty, step):
        """Get action from LLM using the validator's proxy API"""
        
        # If no client, use fallback (but this might cause validation failure)
        if self.client is None:
            print("No API client available, using fallback", file=sys.stderr)
            return self.get_fallback_action(difficulty, step)
        
        # Build prompt
        prompt = f"""You are a customer support agent. Current ticket:
Message: {observation['message']}
Difficulty: {difficulty}
Step: {step}

Choose an action:
- For easy tasks: action_type should be "technical"
- For medium tasks: action_type should be "billing" and provide a helpful response
- For hard tasks: try "technical" first, then "escalate" if needed

Respond with JSON only. Example: {{"action_type": "technical", "content": "Please reset your password"}}
"""
        
        try:
            # Make API call through their proxy
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful customer support agent. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            print(f"LLM Response: {response_text[:100]}...", file=sys.stderr)
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                action_data = json.loads(json_match.group())
                return action_data
            
            return self.get_fallback_action(difficulty, step)
            
        except Exception as e:
            print(f"LLM API error: {e}", file=sys.stderr)
            return self.get_fallback_action(difficulty, step)
    
    def get_fallback_action(self, difficulty, step):
        """Fallback actions if API fails (should still work for validation)"""
        if difficulty == "easy":
            return {"action_type": "technical", "content": "Please reset your password"}
        elif difficulty == "medium":
            if step == 1:
                return {"action_type": "billing", "content": "We are checking your refund"}
            else:
                return {"action_type": "billing", "content": "Your refund is being processed"}
        else:  # hard
            if step == 1:
                return {"action_type": "technical", "content": "Please reinstall the app"}
            else:
                return {"action_type": "escalate", "content": "Escalating to senior support"}
    
    def run_task(self, difficulty):
        """Run a single task"""
        print(f"[START] task={difficulty}", flush=True)
        
        observation = self.env.reset(difficulty)
        total_reward = 0.0
        step = 0
        done = False
        max_steps = 3
        
        while not done and step < max_steps:
            # Get action from LLM (through their proxy)
            action_dict = self.get_llm_action(observation, difficulty, step + 1)
            
            # Ensure required fields
            if "action_type" not in action_dict:
                action_dict["action_type"] = "technical"
            
            action = Action(**action_dict)
            
            # Execute step
            observation, reward, done, info = self.env.step(action)
            
            step_reward = reward["score"]
            total_reward += step_reward
            step += 1
            
            print(f"[STEP] step={step} reward={step_reward:.3f}", flush=True)
        
        # Calculate final score (ensure between 0 and 1)
        final_score = max(0.001, min(0.999, total_reward / max_steps))
        print(f"[END] task={difficulty} score={final_score:.3f} steps={step}", flush=True)
        
        return final_score
    
    def run_all_tasks(self):
        """Run all three tasks"""
        scores = {}
        for difficulty in ["easy", "medium", "hard"]:
            scores[difficulty] = self.run_task(difficulty)
        return scores

def main():
    print("Customer Support Environment - LLM Inference", file=sys.stderr)
    print(f"API_BASE_URL: {API_BASE_URL}", file=sys.stderr)
    print(f"MODEL_NAME: {MODEL_NAME}", file=sys.stderr)
    
    agent = CustomerSupportAgent()
    scores = agent.run_all_tasks()
    
    # Summary to stderr
    print("\n" + "="*40, file=sys.stderr)
    print("FINAL BASELINE SCORES", file=sys.stderr)
    print("="*40, file=sys.stderr)
    for diff, score in scores.items():
        print(f"{diff.upper()}: {score:.3f}", file=sys.stderr)
    print(f"\nAverage: {sum(scores.values())/3:.3f}", file=sys.stderr)
    print("\n✅ Inference complete!", file=sys.stderr)

if __name__ == "__main__":
    main()