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