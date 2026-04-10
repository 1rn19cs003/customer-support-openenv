def grade(actions, task):
    if not actions:
        return 0.0
    
    score = 0.0
    last_action = actions[-1]
    
    # Category check
    if last_action.get("action_type") == task["expected_category"]:
        score += 0.4
    else:
        score -= 0.2
    
    # Reply quality (check all actions for responses)
    best_reply_score = 0.0
    for action in actions:
        if "content" in action and action["content"]:
            reply = action["content"].lower()
            expected = task["expected_reply"].lower()
            
            if expected in reply:
                best_reply_score = 0.4
            elif any(word in reply for word in expected.split()):
                best_reply_score = max(best_reply_score, 0.2)
    
    score += best_reply_score
    
    return max(0.0, min(score, 1.0))