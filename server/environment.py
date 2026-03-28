import random

TICKETS = [
    {
        "message": "I can't login",
        "category": "technical",
        "reply": "Please reset your password",
        "escalate": False
    },
    {
        "message": "Refund not received",
        "category": "billing",
        "reply": "We are checking your refund",
        "escalate": True
    },
    {
        "message": "App is crashing frequently",
        "category": "technical",
        "reply": "Please reinstall the app",
        "escalate": True
    }
]

class MyEnvironment:

    def __init__(self):
        self.ticket = None
        self.done = False

    def reset(self):
        self.ticket = random.choice(TICKETS)
        self.done = False

        return {
            "message": self.ticket["message"]
        }

    def step(self, action):
        reward = 0.0

        # Category match
        if action.action_type == self.ticket["category"]:
            reward += 0.4

        # Reply match
        if action.content and self.ticket["reply"].lower() in action.content.lower():
            reward += 0.4

        # Escalation check
        if action.action_type == "escalate" and self.ticket["escalate"]:
            reward += 0.2

        self.done = True

        return (
            {"message": self.ticket["message"]},
            {"score": reward, "reason": "evaluation"},
            self.done,
            {}
        )

    def state(self):
        return {"ticket": self.ticket}