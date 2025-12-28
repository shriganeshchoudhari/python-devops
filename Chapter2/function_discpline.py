def should_alert(env, status):
    """
    Returns True if alert condition is met:
    - env == "prod"
    - status != "running"
    Otherwise returns False.
    """
    return env == "prod" and status != "running"


# Example usage (no prints inside function, only outside):
print(should_alert("prod", "stopped"))   # True
print(should_alert("prod", "running"))   # False
print(should_alert("dev", "stopped"))    # False