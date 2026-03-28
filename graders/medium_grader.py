def grade(action, task):
    score = 0.0

    # Category check
    if action.get("action_type") == task["expected_category"]:
        score += 0.4
    else:
        score -= 0.2  # penalty

    # Reply quality (fuzzy)
    if "content" in action:
        reply = action["content"].lower()
        expected = task["expected_reply"].lower()

        if expected in reply:
            score += 0.4
        elif any(word in reply for word in expected.split()):
            score += 0.2  # partial credit
        else:
            score -= 0.1

    return max(0.0, min(score, 1.0))