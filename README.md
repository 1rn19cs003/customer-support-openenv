# Customer Support OpenEnv

## Description
This environment simulates a customer support system where an AI agent:
- classifies tickets
- responds to users
- decides escalation

## Actions
- categorize
- reply
- escalate

## Observation
- ticket message

## Reward
- 0.4 category match
- 0.4 reply correctness
- 0.2 escalation decision

## Run locally
uvicorn server.app:app --reload

## Inference
python inference.py