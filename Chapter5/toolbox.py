import sys
import os
import shutil

def file_check(filename: str) -> int:
    if not filename:
        print("Missing filename argument")
        return 2
    if os.path.exists(filename):
        print("FOUND")
        return 0
    else:
        print("NOT FOUND")
        return 1

def env_dir_creator() -> int:
    env = os.environ.get("ENV")
    if not env:
        print("ENV missing")
        return 1
    dir_path = os.path.join("logs", env)
    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory created: {dir_path}")
        return 0
    except Exception as e:
        print(f"Error creating directory: {e}")
        return 1

def safe_backup(filename: str) -> int:
    if not filename:
        print("Missing filename argument")
        return 1
    if not os.path.exists(filename):
        print("Source file does not exist")
        return 1
    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)
    try:
        dest = os.path.join(backup_dir, os.path.basename(filename))
        shutil.copy(filename, dest)
        print(f"File backed up to {dest}")
        return 0
    except Exception as e:
        print(f"Backup failed: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python toolbox.py <command> [args]")
        print("Commands: check <filename>, mkdir, backup <filename>")
        sys.exit(2)

    command = sys.argv[1]

    if command == "check":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(file_check(filename))
    elif command == "mkdir":
        sys.exit(env_dir_creator())
    elif command == "backup":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(safe_backup(filename))
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

if __name__ == "__main__":
    main()