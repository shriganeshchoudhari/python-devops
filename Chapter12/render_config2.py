import logging
from pathlib import Path
import yaml
from jinja2 import Template

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

config = yaml.safe_load(Path("config.yaml").read_text())
template_text = Path("app.conf.j2").read_text()

template = Template(template_text)
output = template.render(**config)

output_path = Path("app.conf")
output_path.write_text(output)

logger.info("Rendered config written to %s", output_path)
