import os
import sys
import shutil

def main():
    if len(sys.argv) < 2:
        print("Missing filename argument")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("Source file does not exist")
        sys.exit(1)

    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)

    try:
        dest = os.path.join(backup_dir, os.path.basename(filename))
        shutil.copy(filename, dest)
        print(f"File backed up to {dest}")
        sys.exit(0)
    except Exception as e:
        print(f"Backup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()