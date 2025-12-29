import os
import sys

def main():
    env = os.environ.get("ENV")

    if not env:
        print("ENV missing")
        sys.exit(1)

    dir_path = os.path.join("logs", env)

    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory created: {dir_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Error creating directory: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()