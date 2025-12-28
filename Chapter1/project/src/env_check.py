import sys
import os

def main():
    print("Python version:", sys.version)
    # print newline   
    print()
    print("Python executable path:", sys.executable)
    print()
    print("Current working directory:", os.getcwd())
    print()
    print("ENV variable (PATH):", os.environ.get("PATH"))

if __name__ == "__main__":
    main()