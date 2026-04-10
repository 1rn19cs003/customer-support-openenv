# server/environment.py
import random
from tasks.easy_task import TASK as EASY_TASK
from tasks.medium_task import TASK as MEDIUM_TASK
from tasks.hard_task import TASK as HARD_TASK
from graders.easy_grader import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader import grade as hard_grade

TASKS = {
    "easy": (EASY_TASK, easy_grade),
    "medium": (MEDIUM_TASK, medium_grade),
    "hard": (HARD_TASK, hard_grade),
}

class MyEnvironment:
    def __init__(self):
        self.current_task = None
        self.current_grader = None
        self.difficulty = None
        self.done = False
        self.step_count = 0
        self.actions_log = []

    def reset(self, difficulty: str = None):
        if difficulty and difficulty in TASKS:
            self.difficulty = difficulty
            self.current_task, self.current_grader = TASKS[difficulty]
        else:
            self.difficulty, (self.current_task, self.current_grader) = random.choice(list(TASKS.items()))
        
        self.done = False
        self.step_count = 0
        self.actions_log = []
        
        return {
            "message": self.current_task["input"],
            "difficulty": self.difficulty
        }

    def step(self, action):
        self.step_count += 1
        
        # Convert to dict if it's a Pydantic model
        if hasattr(action, 'dict'):
            action_dict = action.dict()
        else:
            action_dict = action
        
        self.actions_log.append(action_dict)
        
        # Calculate score
        score = self.current_grader(self.actions_log, self.current_task)
        
        # End after 3 steps or if resolved
        if self.step_count >= 3 or action_dict.get("action_type") == "resolve":
            self.done = True
        
        observation = {
            "message": self.current_task["input"],
            "difficulty": self.difficulty,
            "step": self.step_count,
            "actions_taken": len(self.actions_log)
        }
        
        reward = {
            "score": score,
            "reason": f"Step {self.step_count} graded using {self.difficulty} task"
        }
        
        info = {
            "step": self.step_count,
            "total_actions": len(self.actions_log),
            "difficulty": self.difficulty
        }
        
        return observation, reward, self.done, info

    def state(self):
        return {
            "task": self.current_task,
            "difficulty": self.difficulty,
            "step_count": self.step_count,
            "actions_taken": self.actions_log
        }