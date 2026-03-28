from fastapi import FastAPI
from pydantic import BaseModel
from server.environment import MyEnvironment

app = FastAPI()
env = MyEnvironment()

class Action(BaseModel):
    action_type: str
    content: str | None = None

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()