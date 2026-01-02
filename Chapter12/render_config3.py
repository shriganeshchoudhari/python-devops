import sys
import logging
from pathlib import Path
import yaml
from jinja2 import Template

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if len(sys.argv) != 2:
    logger.error("Usage: python render_config.py <env>")
    sys.exit(1)

env = sys.argv[1]
config_file = Path(f"{env}.yaml")

if not config_file.exists():
    logger.error("Config file not found: %s", config_file)
    sys.exit(1)

config = yaml.safe_load(config_file.read_text())
template = Template(Path("app.conf.j2").read_text())

output = template.render(**config)
out_file = Path(f"app-{env}.conf")
out_file.write_text(output)

logger.info("Rendered %s configuration to %s", env, out_file)
