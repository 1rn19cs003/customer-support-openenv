def grade(actions, task):
    if not actions:
        return 0.001
    
    score = 0.0
    
    # Category check
    category_correct = any(a.get("action_type") == task["expected_category"] for a in actions)
    if category_correct:
        score += 0.3
    else:
        score -= 0.2
    
    # Reply quality
    best_reply_score = 0.0
    for action in actions:
        if "content" in action and action["content"]:
            reply = action["content"].lower()
            expected = task["expected_reply"].lower()
            
            if expected in reply:
                best_reply_score = 0.3
            elif any(word in reply for word in expected.split()):
                best_reply_score = max(best_reply_score, 0.15)
    
    score += best_reply_score
    
    # Escalation decision
    escalated = any(a.get("action_type") == "escalate" for a in actions)
    if task["expected_escalation"]:
        if escalated:
            score += 0.4
        else:
            score -= 0.3
    else:
        if escalated:
            score -= 0.3
    
    # Ensure strictly between 0 and 1
    score = max(0.001, min(0.999, score))
    return score