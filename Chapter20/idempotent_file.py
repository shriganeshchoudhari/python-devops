from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_file_once(path: str):
    p = Path(path)

    if p.exists():
        logger.info("File already exists: %s (no action)", path)
        return

    p.write_text("initial content\n")
    logger.info("File created: %s", path)

def main():
    create_file_once("example.txt")

if __name__ == "__main__":
    main()
