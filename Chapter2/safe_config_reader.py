config = {
    "env": "prod",
    "timeout": 30
}

# Use dict.get() with default for retries
env = config.get("env")
timeout = config.get("timeout")
retries = config.get("retries", 3)

print("env:", env)
print("timeout:", timeout)
print("retries:", retries)