from pydantic import BaseModel

class Observation(BaseModel):
    message: str

class Action(BaseModel):
    action_type: str
    content: str | None = None

class Reward(BaseModel):
    score: float
    reason: str