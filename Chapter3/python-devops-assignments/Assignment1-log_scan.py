from pathlib import Path

def main():
    log_file = Path("app.log")
    if log_file.exists():
        for line in log_file.read_text().splitlines():
            if "ERROR" in line:
                print(line.strip())

if __name__ == "__main__":
    main()