from fastapi import FastAPI
from pydantic import BaseModel
from server.environment import MyEnvironment

app = FastAPI()
env = MyEnvironment()

class Action(BaseModel):
    action_type: str
    content: str | None = None

@app.get("/reset")
@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs
    }

@app.post("/step")
def step(action: dict):
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