import logging
from pathlib import Path
import yaml
from jinja2 import Environment, StrictUndefined

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

config = yaml.safe_load(Path("config.yaml").read_text())

env = Environment(undefined=StrictUndefined)
template = env.from_string(Path("app.conf.j2").read_text())

try:
    output = template.render(**config)
    logger.info("Rendered successfully:\n%s", output)
except Exception as e:
    logger.error("Template rendering failed: %s", e)
