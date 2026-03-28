from fastapi import FastAPI
from pydantic import BaseModel
from server.environment import MyEnvironment
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
env = MyEnvironment()

# Enable CORS for HF space access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for HF spaces
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    action_type: str
    content: str | None = None

@app.get("/debug")
def debug():
    return {"msg": "new code deployed"}

@app.api_route("/reset", methods=["GET", "POST"])
def reset(request: Request):
    print("METHOD:", request.method)

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