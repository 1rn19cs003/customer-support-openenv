# Customer Support OpenEnv Environment

## 🧠 Overview
This project simulates a real-world customer support system where an AI agent must:
- classify incoming tickets
- generate appropriate responses
- decide whether escalation is required

This environment is designed to evaluate agent decision-making using the OpenEnv framework.

---

## 🎯 Objective
The agent interacts with the environment using:
- `reset()` → get new ticket
- `step(action)` → perform action
- `state()` → inspect internal state

---

## 📥 Observation Space
```json
{
  "message": "User issue text"
}