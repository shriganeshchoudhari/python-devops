import yaml
from pathlib import Path

def main():
    config_file = Path("config.yml")
    config = yaml.safe_load(config_file.read_text())

    services = config.get("services", [])
    for service in services:
        print(service)

if __name__ == "__main__":
    main()