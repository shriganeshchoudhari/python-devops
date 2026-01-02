Alright. **Chapter 12.**
This is where ad-hoc scripts either evolve into **configuration management** or die as unmaintainable hacks.

If you hardcode configs after this chapter, you’re doing DevOps wrong.

---

![Image](https://media.geeksforgeeks.org/wp-content/uploads/20231007002636/renderingEngineExplanation-300.png)

![Image](https://learn.microsoft.com/en-us/azure/devops/pipelines/get-started/media/yaml-pipeline-editor/yaml-pipeline-editor-templates.png?view=azure-devops)

![Image](https://www.itsm-docs.com/cdn/shop/products/config6_720x.png?v=1627299944)

![Image](https://www.devopsschool.com/blog/wp-content/uploads/2023/08/1692271823313.gif)

# 📘 CHAPTER 12 — Configuration Files & Templates

**(YAML + Jinja2 — Zero Hardcoding)**

---

## 🎯 Chapter 12 Goal

By the end of this chapter, you must be able to:

* Represent configuration cleanly using YAML
* Separate **data** from **logic**
* Render environment-specific configs using templates
* Generate configs reproducibly for servers, containers, CI

If you mix config values inside Python strings, your code is already rotting.

---

## 1️⃣ YAML — The DevOps Configuration Standard

YAML is used everywhere because:

* Human-readable
* Diff-friendly
* Maps cleanly to Python dicts

### Example YAML (`config.yaml`)

```yaml
env: prod
app:
  name: myapp
  port: 8080
servers:
  - app1
  - app2
```

---

### Loading YAML in Python (SAFE)

```python
import yaml
from pathlib import Path

config = yaml.safe_load(Path("config.yaml").read_text())
```

**Rule:**
Always use `safe_load`.
Anything else is reckless.

---

## 2️⃣ YAML → Python Mental Mapping

| YAML       | Python        |
| ---------- | ------------- |
| key: value | dict          |
| list       | list          |
| nested     | dict of dicts |

```python
config["app"]["port"]
config["servers"][0]
```

If this feels hard, you skipped Chapter 2 mentally.

---

## 3️⃣ Why Templates Exist (Hard Truth)

### ❌ WRONG (hardcoding)

```python
nginx_conf = f"""
server {{
    listen {port};
}}
"""
```

This becomes unreadable fast.

---

### ✅ RIGHT (template)

* Config lives in a template file
* Python injects values
* No string gymnastics

---

## 4️⃣ Jinja2 — The Templating Engine

Install:

```bash
pip install jinja2
```

### Simple template (`app.conf.j2`)

```jinja2
server {
    listen {{ port }};
    server_name {{ name }};
}
```

---

### Render template in Python

```python
from jinja2 import Template

template_text = Path("app.conf.j2").read_text()
template = Template(template_text)

rendered = template.render(
    port=8080,
    name="myapp"
)

Path("app.conf").write_text(rendered)
```

This is **clean, readable, scalable**.

---

## 5️⃣ YAML + Jinja2 (REAL DEVOPS PATTERN)

### YAML (`values.yaml`)

```yaml
app:
  name: myapp
  port: 8080
```

### Template

```jinja2
server {
    listen {{ app.port }};
    server_name {{ app.name }};
}
```

### Python glue

```python
data = yaml.safe_load(Path("values.yaml").read_text())
template = Template(Path("app.conf.j2").read_text())

output = template.render(**data)
```

This pattern is **everywhere**:

* CI pipelines
* Infra templates
* Container configs

---

## 6️⃣ Environment-Specific Configs (STOP COPYING FILES)

### ❌ WRONG

```
config-dev.yaml
config-prod.yaml
config-prod-final.yaml
```

Chaos.

---

### ✅ RIGHT

```yaml
env: prod
app:
  port: 8080
```

Same template, different data.

---

## 7️⃣ Validation — Catch Errors Early

Templates can fail silently if you’re careless.

### Strict rendering

```python
from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined)
template = env.from_string(template_text)
```

Now missing values → **hard failure** (GOOD).

---

## 8️⃣ Common Template Mistakes (STOP THESE)

| Mistake                | Why it’s bad |
| ---------------------- | ------------ |
| Hardcoded values       | Non-reusable |
| Logic in templates     | Unreadable   |
| Multiple env templates | Drift        |
| No validation          | Silent bugs  |

Templates = structure
Python = logic
YAML = data

Mixing roles = mess.

---

# 🧠 ASSIGNMENTS — CHAPTER 12 (MANDATORY)

### 📝 Assignment 1 — YAML Loader

* Create `config.yaml`
* Load it
* Print app name & port using logging

---

### 📝 Assignment 2 — Template Renderer

* Create a `.j2` template
* Render it using YAML values
* Write output to file

---

### 📝 Assignment 3 — Environment Switch

* Use one template
* Two YAML files (`dev.yaml`, `prod.yaml`)
* Generate two outputs

---

### 📝 Assignment 4 — Strict Failure

* Enable `StrictUndefined`
* Prove template fails if value missing

---
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

## ✅ Chapter 12 Exit Criteria

You move on ONLY if:

* No hardcoded config values exist
* YAML drives behavior
* Templates are reusable
* Missing values fail fast

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 13 — Docker Automation with Python**

This is where configs meet **containers**.

Reply with:

1. Your rendered template output
2. YAML used
3. One sentence: **why templates beat hardcoding**

Then we continue.
