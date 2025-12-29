import json
import sys
import os

def main():
    config_file = "config.json"

    # Check if file exists
    if not os.path.exists(config_file):
        print("Config file missing")
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

    # Check for 'env' key
    env = config.get("env")
    if not env:
        print("Environment missing in config")
        sys.exit(2)

    print("Config OK")
    sys.exit(0)

if __name__ == "__main__":
    main()