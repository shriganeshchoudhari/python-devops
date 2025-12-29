import sys


def load_config():
    # Dummy implementation for illustration purposes
    raise FileNotFoundError("Configuration file not found")

try:
    config = load_config()
except FileNotFoundError:
    print("Config missing")
    sys.exit(1)
except ValueError as e:
    print(e)
    sys.exit(2)

print("Config OK")
sys.exit(0)
