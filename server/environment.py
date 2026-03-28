import random

from tasks.easy_task import TASK as EASY_TASK
from tasks.medium_task import TASK as MEDIUM_TASK
from tasks.hard_task import TASK as HARD_TASK

from graders.easy_grader import grade as easy_grade
from graders.medium_grader import grade as medium_grade
from graders.hard_grader import grade as hard_grade


TASKS = [
    ("easy", EASY_TASK, easy_grade),
    ("medium", MEDIUM_TASK, medium_grade),
    ("hard", HARD_TASK, hard_grade),
]


class MyEnvironment:

    def __init__(self):
        self.current_task = None
        self.current_grader = None
        self.difficulty = None
        self.done = False

    def reset(self):
        self.difficulty, self.current_task, self.current_grader = random.choice(TASKS)
        self.done = False

        return {
            "message": self.current_task["input"],
            "difficulty": self.difficulty
        }

    def step(self, action):
        score = self.current_grader(action.dict(), self.current_task)

        self.done = True

        return (
            {
                "message": self.current_task["input"],
                "difficulty": self.difficulty
            },
            {
                "score": score,
                "reason": f"Graded using {self.difficulty} task"
            },
            self.done,
            {}
        )

    def state(self):
        return {
            "task": self.current_task,
            "difficulty": self.difficulty
        }