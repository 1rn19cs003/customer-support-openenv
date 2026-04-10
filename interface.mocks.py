"""
Inference Script with Mock Agent (No API Key Required)
Use this for testing the structured output format
"""

import sys
import random
from server.environment import MyEnvironment

sys.stdout.reconfigure(line_buffering=True)

class MockAgent:
    def __init__(self):
        self.env = MyEnvironment()
    
    def get_mock_action(self, difficulty, step):
        # Simple rule-based actions
        if difficulty == "easy":
            return {"action_type": "technical", "content": "Please reset your password"}
        elif difficulty == "medium":
            return {"action_type": "billing", "content": "We are checking your refund"}
        else:  # hard
            # Sometimes escalate, sometimes technical
            if step > 1:
                return {"action_type": "escalate", "content": "Escalating to senior support"}
            return {"action_type": "technical", "content": "Please reinstall the app"}
    
    def run_task(self, difficulty):
        print(f"[START] task={difficulty}", flush=True)
        
        observation = self.env.reset(difficulty)
        total_reward = 0.0
        step = 0
        done = False
        
        while not done and step < 3:
            action_dict = self.get_mock_action(difficulty, step + 1)
            
            # Convert to Action object if needed
            from pydantic import BaseModel
            class Action(BaseModel):
                action_type: str
                content: str | None = None
            
            action = Action(**action_dict)
            observation, reward, done, info = self.env.step(action)
            
            step_reward = reward["score"]
            total_reward += step_reward
            step += 1
            
            print(f"[STEP] step={step} reward={step_reward:.3f}", flush=True)
        
        final_score = min(1.0, total_reward / 3.0)
        print(f"[END] task={difficulty} score={final_score:.3f} steps={step}", flush=True)
        
        return final_score
    
    def run_all_tasks(self):
        scores = {}
        for difficulty in ["easy", "medium", "hard"]:
            scores[difficulty] = self.run_task(difficulty)
        return scores

def main():
    agent = MockAgent()
    scores = agent.run_all_tasks()
    
    # Summary to stderr
    print("\n" + "="*40, file=sys.stderr)
    print("FINAL BASELINE SCORES", file=sys.stderr)
    print("="*40, file=sys.stderr)
    for diff, score in scores.items():
        print(f"{diff.upper()}: {score:.3f}", file=sys.stderr)
    print(f"\nAverage: {sum(scores.values())/3:.3f}", file=sys.stderr)

if __name__ == "__main__":
    main()