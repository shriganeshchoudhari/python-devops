import subprocess
import sys

def main():
    try:
        # Intentionally run a failing command
        subprocess.run(["false"], check=True)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()