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
  "difficulty": "easy | medium | hard"
}