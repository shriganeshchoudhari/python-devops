import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MemoryMonitor")

def check_memory(threshold=60):
    mem = psutil.virtual_memory()
    percent = mem.percent
    logger.info(f"Memory usage: {percent}%")
    return percent <= threshold

if __name__ == "__main__":
    ok = check_memory()
    exit(0 if ok else 1)