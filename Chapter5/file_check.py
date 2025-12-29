import sys
import os

def main():
    # Check if filename argument is provided
    if len(sys.argv) < 2:
        print("Missing filename argument")
        sys.exit(2)

    filename = sys.argv[1]

    if os.path.exists(filename):
        print("FOUND")
        sys.exit(0)
    else:
        print("NOT FOUND")
        sys.exit(1)

if __name__ == "__main__":
    main()