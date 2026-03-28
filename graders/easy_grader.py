def grade(action, task):
    if action["action_type"] == task["expected_category"]:
        return 1.0
    return 0.0