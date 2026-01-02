import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

config_path = Path("config.yaml")
config = yaml.safe_load(config_path.read_text())

logger.info("App Name: %s", config["app"]["name"])
logger.info("App Port: %s", config["app"]["port"])
