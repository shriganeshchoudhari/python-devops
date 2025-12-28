
# 📘 CHAPTER 3 — Strings, Files & Paths (REAL DevOps Usage)

This chapter separates:

* people who *know Python*
* from people who can **handle configs, logs, and files safely in production**

Most outages caused by scripts come from **bad string handling or bad paths**.

---

## 🎯 Chapter 3 Goal

By the end of this chapter, you must be able to:

* Manipulate strings safely (no fragile hacks)
* Read & write files without assuming locations
* Handle JSON/YAML configs
* Use paths that work on **Windows + Linux + containers**

If you hardcode paths or blindly split strings, your code is garbage.

---

## 1️⃣ Strings — Stop Treating Them Like Text Only

In DevOps, strings represent:

* file paths
* shell commands
* hostnames
* logs
* config values

### String basics you MUST control

```python
service = "nginx"
env = "prod"
```

---

### f-strings (MANDATORY)

```python
print(f"Deploying {service} to {env}")
```

❌ If you use `+` for concatenation, stop.

---

### Common string operations (REAL use)

```python
log = "ERROR: disk full on app1"

log.startswith("ERROR")
log.endswith("app1")
"log" in log
log.lower()
```

---

### Splitting logs (carefully)

```python
parts = log.split(":")
level = parts[0]
message = parts[1].strip()
```

⚠️ Brutal truth:
Blind `.split()` without checks = runtime crashes.

---

## 2️⃣ Paths — This Is Where Windows & Linux Break Scripts

### ❌ WRONG (DO NOT DO THIS)

```python
path = "C:\\logs\\app.log"
path = "/var/log/app.log"
```

Hardcoded paths = broken automation.

---

## ✅ Correct Way — `pathlib` (NON-NEGOTIABLE)

```python
from pathlib import Path

log_path = Path("logs") / "app.log"
print(log_path)
```

Why this matters:

* Works on Windows
* Works on Linux
* Works in Docker
* No string hacks

---

### Absolute vs Relative paths

```python
Path.cwd()          # current working directory
Path(__file__)      # current file
Path(__file__).parent
```

### DevOps-safe pattern

```python
BASE_DIR = Path(__file__).parent
config_path = BASE_DIR / "config.yaml"
```

---

## 3️⃣ Reading Files — Safely

### Read text file

```python
with open("example.txt", "r") as f:
    content = f.read()
```

### Line-by-line (logs)

```python
with open("app.log") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

Why `with` matters:

* File closes automatically
* Prevents file locks (important on Windows)

---

## 4️⃣ Writing Files — Without Corruption

```python
with open("output.txt", "w") as f:
    f.write("Deployment successful\n")
```

Append mode:

```python
with open("output.txt", "a") as f:
    f.write("Another entry\n")
```

---

## 5️⃣ JSON — API & Config Backbone

### JSON = dict + list

```python
import json

data = {
    "env": "prod",
    "timeout": 30
}
```

### Write JSON

```python
with open("config.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Read JSON

```python
with open("config.json") as f:
    config = json.load(f)

print(config["env"])
```

📌 Almost every API response becomes JSON → dict.

---

## 6️⃣ YAML — DevOps Native Language

Used in:

* Kubernetes
* Ansible
* Helm
* CI pipelines

### Install dependency

```bash
pip install pyyaml
```

### Read YAML

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

print(config)
```

⚠️ ALWAYS use `safe_load`, never `load`.

---

## 7️⃣ Encoding & Newlines (Windows Gotcha)

```python
with open("file.txt", encoding="utf-8") as f:
    content = f.read()
```

If you ignore encoding:

* Works on Linux
* Fails on Windows
* Breaks CI

---

## 8️⃣ Common DevOps Mistakes (DO NOT COMMIT THESE)

| Mistake            | Why it’s bad           |
| ------------------ | ---------------------- |
| Hardcoded paths    | Cross-platform failure |
| String-built paths | Fragile                |
| No `with open`     | File leaks             |
| Ignoring encoding  | Windows bugs           |
| Blind `.split()`   | Runtime crashes        |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Log Error Scanner

Create `log_scan.py`:

* Read a file `app.log`
* Print only lines containing `ERROR`
* Use `pathlib`
* Strip newlines

---

### 📝 Assignment 2 — Config Loader

Create `config.json`:

```json
{
  "env": "prod",
  "timeout": 20
}
```

Write Python code that:

* Reads config
* Prints env
* Prints timeout
* Prints retries (default = 3 if missing)

---

### 📝 Assignment 3 — YAML Reader

Create `config.yaml`:

```yaml
env: dev
services:
  - nginx
  - redis
```

Write code to:

* Load YAML
* Loop services
* Print each service

---
Here you go Ganesh — clean Python solutions for each mandatory assignment:

---

## 📝 Assignment 1 — Log Error Scanner (`log_scan.py`)

```python
from pathlib import Path

def main():
    log_file = Path("app.log")
    if log_file.exists():
        for line in log_file.read_text().splitlines():
            if "ERROR" in line:
                print(line.strip())

if __name__ == "__main__":
    main()
```

---

## 📝 Assignment 2 — Config Loader (`config.json` + Python code)

**config.json**
```json
{
  "env": "prod",
  "timeout": 20
}
```

**Python code:**
```python
import json
from pathlib import Path

def main():
    config_file = Path("config.json")
    config = json.loads(config_file.read_text())

    env = config.get("env")
    timeout = config.get("timeout")
    retries = config.get("retries", 3)

    print("env:", env)
    print("timeout:", timeout)
    print("retries:", retries)

if __name__ == "__main__":
    main()
```

---

## 📝 Assignment 3 — YAML Reader (`config.yaml` + Python code)

**config.yaml**
```yaml
env: dev
services:
  - nginx
  - redis
```

**Python code:**
```python
import yaml
from pathlib import Path

def main():
    config_file = Path("config.yaml")
    config = yaml.safe_load(config_file.read_text())

    services = config.get("services", [])
    for service in services:
        print(service)

if __name__ == "__main__":
    main()
```

---

✨ These scripts give you:
- A **log scanner** that filters only `ERROR` lines.
- A **config loader** with safe defaults.
- A **YAML reader** that loops through services.

Would you like me to also bundle these into a **single repo-style structure** (with `requirements.txt` and README) so you can run them as a mini DevOps exercise?


Here’s a neat **repo-style structure** you can drop straight into your DevOps practice folder. It includes the three assignments, a `requirements.txt`, and a `README.md` for reproducibility.

---

### 📂 Project Layout
```
python-devops-assignments/
├── Assignment1-log_scan.py
├── Assignment2-config_loader.py
├── Assignment3-yaml_reader.py
├── app.log
├── config.json
├── config.yaml
├── requirements.txt
└── README.md
```

---

### ✅ Files

**Assignment1-log_scan.py**
```python
from pathlib import Path

def main():
    log_file = Path("app.log")
    if log_file.exists():
        for line in log_file.read_text().splitlines():
            if "ERROR" in line:
                print(line.strip())

if __name__ == "__main__":
    main()
```

**Assignment2-config_loader.py**
```python
import json
from pathlib import Path

def main():
    config_file = Path("config.json")
    config = json.loads(config_file.read_text())

    env = config.get("env")
    timeout = config.get("timeout")
    retries = config.get("retries", 3)

    print("env:", env)
    print("timeout:", timeout)
    print("retries:", retries)

if __name__ == "__main__":
    main()
```

**Assignment3-yaml_reader.py**
```python
import yaml
from pathlib import Path

def main():
    config_file = Path("config.yaml")
    config = yaml.safe_load(config_file.read_text())

    services = config.get("services", [])
    for service in services:
        print(service)

if __name__ == "__main__":
    main()
```

---

### 📄 Sample Data Files

**app.log**
```
INFO Starting application
ERROR Failed to connect to database
INFO Retrying connection
ERROR Timeout occurred
```

**config.json**
```json
{
  "env": "prod",
  "timeout": 20
}
```

**config.yaml**
```yaml
env: dev
services:
  - nginx
  - redis
```

---

### 📦 requirements.txt
```
PyYAML==6.0.2
```

---

### 📘 README.md
```markdown
# Python DevOps Assignments

## Setup
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Assignment 1 — Log Error Scanner
Run:
```bash
python Assignment1-log_scan.py
```
Prints only lines containing `ERROR` from `app.log`.

## Assignment 2 — Config Loader
Run:
```bash
python Assignment2-config_loader.py
```
Prints `env`, `timeout`, and `retries` (default = 3 if missing).

## Assignment 3 — YAML Reader
Run:
```bash
python Assignment3-yaml_reader.py
```
Loops through services in `config.yaml` and prints each one.
```

---

✨ This repo setup is modular and reproducible. You can zip it, push to GitHub, or run directly in your DevOps exercises.  

Do you want me to also add a **Makefile** or **run.sh** script so you can execute all assignments with a single command?

## ✅ Chapter 3 Exit Criteria (STRICT)

You move forward ONLY if:

* You use `pathlib`, not string paths
* You successfully read/write JSON
* You successfully read YAML
* Your scripts work on Windows paths

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 4 — Error Handling & Exit Codes (Production Safety)**

Reply with:

1. Your code for all 3 assignments
2. Any raw errors
3. Confirmation you understand **why pathlib is mandatory**

No rushing.
Do it properly — or we fix it before moving on.
