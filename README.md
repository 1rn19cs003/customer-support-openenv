---
title: customer-support-env
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 8000
---

# Customer Support OpenEnv Environment

## 🚀 Overview

This project simulates a **real-world customer support system**, where an AI agent must handle incoming user queries such as refunds, complaints, and technical issues.

The environment is designed using the OpenEnv framework and evaluates how effectively an AI agent:
- Understands customer intent
- Chooses the correct action
- Provides meaningful responses

---

## 🧠 Problem Motivation

Customer support automation is a **real industry problem**.
This environment mimics real workflows like:
- Refund handling
- Complaint resolution
- Query classification

It helps evaluate LLM agents in **practical business scenarios**, not toy problems.

---

## ⚙️ OpenEnv Interface

## HuggingFace Url
`https://abhi13082000-customer-support-env.hf.space/${Objective}`

## 🎯 Objective
The agent interacts with the environment using:
- `reset()` → get new ticket
- `step(action)` → perform action
- `state()` → inspect internal state

### Observation

```json
{
  "message": "Customer query",
  "difficulty": "easy | medium | hard",
  "step": 1,
  "actions_taken": 0
}
```

### Actions

Actions are JSON objects with the following structure:

```json
{
  "action_type": "technical | billing | complaint | general",
  "content": "Optional response message to customer"
}
```

**Action Types:**
- `technical` - For technical issues (login problems, bugs, etc.)
- `billing` - For refund, payment, or billing issues
- `complaint` - For customer complaints or escalations
- `general` - For general inquiries

### Reward

```json
{
  "score": 0.0-1.0,
  "reason": "Step X graded using difficulty task"
}
```

Rewards are based on:
- Correct action type selection
- Quality of response content (for medium/hard tasks)
- Proper resolution handling

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip or uv package manager

### Local Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd customer_support_env
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
# or using uv
uv pip install -r requirements.txt
```

3. **Set up environment variables (optional):**
Create a `.env` file for API keys if needed:
```bash
# .env
OPENAI_API_KEY=your_key_here
```

---

## 🚀 Running the Environment

### Local Development

**Start the server:**
```bash
# Using Python module
python -m server.app

# Or using uvicorn directly
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Using Docker

**Build and run:**
```bash
docker build -t customer-support-env .
docker run -p 8000:8000 customer-support-env
```

### Testing the Environment

**Reset to get a new ticket:**
```bash
curl http://localhost:8000/reset
```

**Take an action:**
```bash
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "technical", "content": "I will help you with your login issue"}'
```

**Check current state:**
```bash
curl http://localhost:8000/state
```

---

## 🤖 Using with AI Agents

### Python Client Example

```python
from client import CustomerSupportEnv

# Connect to local server
with CustomerSupportEnv(base_url="http://localhost:8000") as env:
    # Get a new ticket
    result = env.reset()
    print(f"Customer query: {result.observation.message}")
    print(f"Difficulty: {result.observation.difficulty}")

    # Take an action
    from models import Action
    action = Action(action_type="technical", content="I'll help with your login")
    result = env.step(action)

    print(f"Reward: {result.reward.score}")
    print(f"Done: {result.done}")
```

### OpenAI Integration Example

```python
import openai
from client import CustomerSupportEnv

client = openai.OpenAI()
env = CustomerSupportEnv(base_url="http://localhost:8000")

# Reset environment
obs = env.reset()

# Use LLM to determine action
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"Customer says: {obs.observation.message}\n\nRespond with action_type and content."
    }]
)

# Parse and execute action
# ... (implementation depends on your parsing logic)
```

---

## 🌐 Hugging Face Deployment

### Prerequisites
- Hugging Face account
- OpenEnv CLI installed

### Deploy to Hugging Face Spaces

1. **Install OpenEnv CLI:**
```bash
pip install openenv-cli
```

2. **Login to Hugging Face:**
```bash
huggingface-cli login
```

3. **Push to Hugging Face:**
```bash
openenv push --repo-id abhi13082000/customer-support-env
```

This will:
- Create/update the Hugging Face Space
- Deploy the Docker container
- Make the environment available at: `https://abhi13082000-customer-support-env.hf.space`

### Using the Deployed Environment

Once deployed, you can interact with it using the same API:

```python
from client import CustomerSupportEnv

# Connect to HF Space
env = CustomerSupportEnv(base_url="https://abhi13082000-customer-support-env.hf.space")
# Use same interface as local
```

---

## 📊 Task Difficulties

### Easy Tasks
- Simple classification
- Single action required
- Example: "I can't login to my account" → `technical`

### Medium Tasks
- Classification + response quality
- Multiple steps may be needed
- Example: "Refund not received" → `billing` + appropriate response

### Hard Tasks
- Complex scenarios
- Multiple actions and responses
- Higher reasoning required

---

## 🔧 Development

### Project Structure
```
customer_support_env/
├── server/
│   ├── app.py              # FastAPI server
│   └── environment.py      # Environment logic
├── tasks/                  # Task definitions
├── graders/                # Scoring functions
├── client.py               # Python client
├── models.py               # Data models
├── inference.py            # LLM integration example
└── Dockerfile              # Container definition
```

### Adding New Tasks

1. Create task in `tasks/your_task.py`:
```python
TASK = {
    "input": "Your customer query here",
    "expected_category": "action_type",
    "expected_reply": "Expected response content"
}
```

2. Create grader in `graders/your_grader.py`:
```python
def grade(actions, task):
    # Your scoring logic
    return score  # 0.001 to 0.999
```

3. Update `server/environment.py` to include new task.

---

## 📝 License

This project is licensed under the BSD-style license. See LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

For questions or issues, please open a GitHub issue.