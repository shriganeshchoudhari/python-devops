import logging
from typing import Optional

def setup_logging(level: int = logging.INFO, name: str = "release_sentinel") -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger