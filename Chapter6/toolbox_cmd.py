import sys
import subprocess

def run_command(cmd: list) -> int:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print("Exit Code:", result.returncode)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return 1

def validate_tool() -> int:
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
            return 0
        else:
            print("Git not found or error running git")
            return 1
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        return 1

def fail_fast() -> int:
    try:
        subprocess.run(["false"], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python toolbox_cmd.py <command> [args...]")
        print("Commands: run <cmd...>, validate, fail")
        sys.exit(2)

    command = sys.argv[1]

    if command == "run":
        if len(sys.argv) < 3:
            print("Missing command to run")
            sys.exit(2)
        sys.exit(run_command(sys.argv[2:]))
    elif command == "validate":
        sys.exit(validate_tool())
    elif command == "fail":
        sys.exit(fail_fast())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

if __name__ == "__main__":
    main()