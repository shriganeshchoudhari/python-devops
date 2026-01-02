You want **solutions**, not hints. Fine.
Below is **clean, production-grade solution code** for **ALL Chapter 12 assignments**.
Read it carefully — don’t just copy-paste blindly.

---

# ✅ CHAPTER 12 — ASSIGNMENT SOLUTIONS

(YAML + Jinja2)

---

## 📁 Folder Structure (MANDATORY)

```
chapter12/
├── config.yaml
├── dev.yaml
├── prod.yaml
├── app.conf.j2
├── render_config.py
└── strict_render.py
```

If your structure is messier than this, you’re already drifting.

---

## 📝 Assignment 1 — YAML Loader

### `config.yaml`

```yaml
app:
  name: myapp
  port: 8080
```

### `render_config.py` (part 1)

```python
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
```

---

## 📝 Assignment 2 — Template Renderer

### `app.conf.j2`

```jinja2
server {
    listen {{ app.port }};
    server_name {{ app.name }};
}
```

### `render_config.py` (part 2 – full file)

```python
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
```

---

## 📝 Assignment 3 — Environment Switch (DEV / PROD)

### `dev.yaml`

```yaml
app:
  name: myapp-dev
  port: 8081
```

### `prod.yaml`

```yaml
app:
  name: myapp-prod
  port: 80
```

### `render_config.py` (env-aware version)

```python
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
```

Run:

```bash
python render_config.py dev
python render_config.py prod
```

---

## 📝 Assignment 4 — Strict Failure (NO SILENT BUGS)

### `strict_render.py`

```python
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
```

### 🔥 Test failure on purpose

Remove `port` from `config.yaml`:

```yaml
app:
  name: myapp
```

Run:

```bash
python strict_render.py
```

It **must fail loudly**.
If it doesn’t — your setup is broken.

---

## ✅ CHAPTER 12 — FINAL CHECKLIST

You are **done** with this chapter if:

* ✅ No hardcoded config values
* ✅ YAML controls behavior
* ✅ Jinja2 renders templates
* ✅ StrictUndefined catches missing values
* ✅ Same template works for multiple envs

If you can explain **why this pattern scales**, you’re thinking like DevOps.

---

## 🚀 NEXT CHAPTER (NO GOING BACK)

➡ **Chapter 13 — Docker Automation with Python**

This is where:

* Python meets Docker Engine
* Scripts build images
* Containers get inspected, started, stopped

