import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fail_loudly.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            _ = f.read()
        sys.exit(0)
    except Exception as e:
        print(f"Failed to read file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()