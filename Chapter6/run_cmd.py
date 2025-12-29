import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_cmd.py <command> [args...]")
        sys.exit(2)

    cmd = sys.argv[1:]  # command and args as list

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print("Exit Code:", result.returncode)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()