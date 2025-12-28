import json
from pathlib import Path

def main():
    config_file = Path("config.json")
    config = json.loads(config_file.read_text())

    env = config.get("env")
    timeout = config.get("timeout")
    retries = config.get("retries", 3)

    print("env:", env)
    print("timeout:", timeout)
    print("retries:", retries)

if __name__ == "__main__":
    main()