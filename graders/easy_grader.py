def grade(actions, task):
    if not actions:
        return 0.001  # Slightly above 0
    
    last_action = actions[-1]
    
    if last_action.get("action_type") == task["expected_category"]:
        return 0.999  # Slightly below 1
    return 0.001