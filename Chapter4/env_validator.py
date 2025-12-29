import sys

def validate_env(env: str) -> None:
    allowed = {"dev", "stage", "prod"}
    if env not in allowed:
        raise ValueError(f"Invalid environment: {env}")
try:
    validate_env("test")  # invalid
except ValueError as e:
    print(e)
    sys.exit(2)