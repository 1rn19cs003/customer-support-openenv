def grade(actions, task):
    # actions is a list of action dictionaries
    if not actions:
        return 0.0
    
    # Check the most recent action
    last_action = actions[-1]
    
    if last_action.get("action_type") == task["expected_category"]:
        return 1.0
    return 0.0