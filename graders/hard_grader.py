def grade(action, task):
    score = 0.0

    # Category
    if action.get("action_type") == task["expected_category"]:
        score += 0.3
    else:
        score -= 0.2

    # Reply quality
    if "content" in action:
        reply = action["content"].lower()
        expected = task["expected_reply"].lower()

        if expected in reply:
            score += 0.3
        elif any(word in reply for word in expected.split()):
            score += 0.15
        else:
            score -= 0.1

    # Escalation decision
    if task["expected_escalation"]:
        if action.get("action_type") == "escalate":
            score += 0.4
        else:
            score -= 0.3
    else:
        if action.get("action_type") == "escalate":
            score -= 0.3

    return max(0.0, min(score, 1.0))