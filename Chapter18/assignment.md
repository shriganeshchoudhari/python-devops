Good. This chapter is **high-risk**, so I’ll give you **exact solutions + why each line exists**.
If you copy this blindly without understanding, you’ll still leak secrets later. Read carefully.

---

# ✅ CHAPTER 18 — Secrets & Security

**(Solutions + Explanations)**

---

## 📁 Recommended Structure

```
chapter18/
├── .gitignore
├── .env
├── env_secret_loader.py
├── dotenv_loader.py
├── ci_simulation.py
└── secret_fetch_stub.py
```

---

## 📝 Assignment 1 — Environment Secret Loader

### Goal

* Read secret from environment
* Fail loudly if missing
* **Never print the secret**

---

### `env_secret_loader.py`

```python
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    api_key = os.getenv("API_KEY")

    if not api_key:
        logger.error("API_KEY is not set")
        sys.exit(1)

    logger.info("API_KEY loaded successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this is correct

* `os.getenv()` → standard, portable, CI-safe
* No default value → **fail closed**
* Logging confirms presence **without exposure**
* Exit code controls CI behavior

❌ Printing the key here would already be a security incident.

---

## 📝 Assignment 2 — `.env` Safety (Local-Only Secrets)

### `.env`

```
API_KEY=local-secret-123
```

### `.gitignore`

```
.env
```

This is **mandatory**. If `.env` is not ignored, stop immediately.

---

### `dotenv_loader.py`

```python
import sys
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()  # loads .env into environment

    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY not found in .env")
        sys.exit(1)

    logger.info("API_KEY loaded from .env safely")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this exists

* `.env` is **developer convenience only**
* Keeps secrets out of code
* CI & prod should **not** use `.env`

🚫 If `.env` ever reaches Git, rotate all secrets immediately.

---

## 📝 Assignment 3 — CI Simulation (Env Injection)

### `ci_simulation.py`

```python
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    token = os.getenv("DEPLOY_TOKEN")

    if not token:
        logger.error("DEPLOY_TOKEN missing — CI must stop")
        sys.exit(1)

    logger.info("DEPLOY_TOKEN detected (value not logged)")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### How to test (Windows)

```bat
set DEPLOY_TOKEN=ci-secret
python ci_simulation.py
```

Then:

```bat
set DEPLOY_TOKEN=
python ci_simulation.py
```

### Why this matters

* CI injects secrets **at runtime**
* Script must behave the same locally & in CI
* Missing secret = **hard failure**

CI that “warns and continues” is lying.

---

## 📝 Assignment 4 — Secret Fetch Stub (Vault-Style Pattern)

### Goal

Simulate secure secret retrieval **without storing secrets**.

---

### `secret_fetch_stub.py`

```python
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_secret():
    token = os.getenv("VAULT_TOKEN")

    if not token:
        raise RuntimeError("VAULT_TOKEN not set")

    # Simulated secure fetch
    # In real life, this would be an API call
    secret = "fetched-secret-value"

    return secret

def main():
    try:
        _ = fetch_secret()
        logger.info("Secret fetched successfully")
        sys.exit(0)
    except Exception as e:
        logger.error("Secret fetch failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Why this pattern is critical

* Token comes from env (never code)
* Secret fetched **at runtime**
* Secret never logged
* Function can be replaced with real Vault logic later

This is how production systems access secrets safely.

---

## 🔥 Common Mistakes You AVOIDED (Good)

| Mistake                      | Why it’s deadly   |
| ---------------------------- | ----------------- |
| Hardcoding secrets           | Permanent leak    |
| Printing secrets             | Log-based breach  |
| Using `.env` in prod         | Weak security     |
| Default secret values        | Silent compromise |
| Continuing on missing secret | Unsafe deployment |

---

## 🧠 Mental Model (Memorize This)

* **Config** → can be committed
* **Secrets** → must be injected
* **Logs** → assume public
* **Code** → assume leaked

Therefore:

> Secrets must **never trust humans**.

Humans copy, paste, screenshot, commit, and forget.

---

## ✅ Chapter 18 — FINAL VERDICT

You now understand:

* Why env vars are the baseline
* Why `.env` is local-only
* Why CI must fail on missing secrets
* Why secrets are fetched, not stored
* Why logging discipline is non-negotiable

This is **career-saving knowledge**.

---

## 🚀 NEXT CHAPTER

➡ **Chapter 19 — Python for Monitoring & Alerting**

This is where:

* scripts watch systems
* thresholds matter
* alerts wake people up

---

## 📝 Unified Script: `secrets_toolbox.py`

```python
import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SecretsToolbox")


# --- Assignment 1: Env Secret Loader ---
def load_env_secret():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("Missing API_KEY in environment")
        return 1
    logger.info("API_KEY loaded successfully (value hidden)")
    return 0


# --- Assignment 2: .env Safety ---
def load_dotenv_secret():
    if not os.path.exists(".env"):
        logger.error(".env file missing — secrets not loaded")
        return 1

    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("API_KEY missing in .env")
        return 1

    logger.info("Secrets loaded from .env (values hidden)")
    return 0


# --- Assignment 3: CI Simulation ---
def ci_simulation():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("CI Simulation failed — API_KEY not set")
        return 1
    logger.info("CI Simulation success — API_KEY present (value hidden)")
    return 0


# --- Assignment 4: Secret Fetch Stub ---
def fetch_secret():
    token = os.environ.get("TOKEN")
    if not token:
        logger.error("Missing TOKEN in environment")
        return None

    # Simulate API fetch without revealing token
    logger.info("Fetched secret successfully (value hidden)")
    return {"status": "ok", "data": "simulated response"}


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: secrets_toolbox.py [load|dotenv|ci|fetch]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "load":
        sys.exit(load_env_secret())
    elif cmd == "dotenv":
        sys.exit(load_dotenv_secret())
    elif cmd == "ci":
        sys.exit(ci_simulation())
    elif cmd == "fetch":
        result = fetch_secret()
        sys.exit(0 if result else 1)
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

## 🚀 Step‑Wise Execution

### 1. Env Secret Loader
```bash
export API_KEY=12345        # Linux/macOS
$env:API_KEY="12345"        # Windows PowerShell
python secrets_toolbox.py load
```
Logs success if `API_KEY` is set.

---

### 2. .env Safety
- Create `.env` file:
  ```
  API_KEY=12345
  ```
- Add `.env` to `.gitignore`:
  ```
  .env
  ```
- Run:
  ```bash
  python secrets_toolbox.py dotenv
  ```
Fails if `.env` missing, succeeds if present.

---

### 3. CI Simulation
```bash
export API_KEY=12345
python secrets_toolbox.py ci
unset API_KEY
python secrets_toolbox.py ci
```
First run succeeds, second run fails — simulating CI pipeline.

---

### 4. Secret Fetch Stub
```bash
export TOKEN=abc123
python secrets_toolbox.py fetch
```
Logs success, returns simulated response, never prints token.

---

✅ Now you’ve got a **single secrets toolbox** that handles environment secrets, `.env` safety, CI simulation, and secret fetch stubs — all with proper logging and exit codes.  

