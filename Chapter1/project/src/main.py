import os

def main():
    print("Python for DevOps started correctly")
    env = os.getenv("ENV", "default")
    print(env)

if __name__ == "__main__":
    main()
