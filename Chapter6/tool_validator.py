import subprocess
import sys

def main():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
            sys.exit(0)
        else:
            print("Git not found or error running git")
            sys.exit(1)
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        sys.exit(1)

if __name__ == "__main__":
    main()