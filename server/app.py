from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from server.environment import MyEnvironment

app = FastAPI()
env = MyEnvironment()

# Enable CORS for HF
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    action_type: str
    content: str | None = None

@app.api_route("/reset", methods=["GET", "POST"])
def reset(request: Request):
    obs = env.reset()
    return {"observation": obs}

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
def state():
    return env.state()


def main():
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()