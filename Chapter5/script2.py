import sys

if len(sys.argv) < 2:
    print("Filename required")
    print(sys.executable)
    print(sys.platform)

    sys.exit(1)

filename = sys.argv[1]
