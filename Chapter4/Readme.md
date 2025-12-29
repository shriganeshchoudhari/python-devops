We move on — but understand this clearly:

**Chapter 4 is where scripts stop being toys and start being production-safe.**
If you screw this up, your automation will:

* silently fail
* break CI
* lie about success

That’s worse than crashing.

---

# 📘 CHAPTER 4 — Error Handling & Exit Codes (PRODUCTION SAFETY)

This chapter is **non-negotiable** for DevOps.

---

## 🎯 Chapter 4 Goal

By the end of this chapter, you must:

* Predict where things can fail
* Catch only what you can handle
* Fail loudly when you must
* Return correct exit codes to CI / shell

If your script always exits with `0`, it’s **lying**.

---

## 1️⃣ Exceptions — What They Really Are

An exception is:

> Python screaming “this is unsafe, stop now”

### Example failure

```python
int("abc")  # ValueError
```

If you don’t handle it:

* Script crashes
* Pipeline fails (sometimes good, sometimes bad)

Your job is to decide **which failures are acceptable**.

---

## 2️⃣ try / except — Controlled Failure

### ❌ WRONG (swallowing errors)

```python
try:
    risky()
except:
    pass
```

This is **criminally bad**.
You just hid a failure.

---

### ✅ Correct pattern

```python
try:
    value = int("123")
except ValueError as e:
    print(f"Invalid number: {e}")
```

Rules:

* Catch **specific exceptions**
* Do something meaningful
* Never hide errors silently

---

## 3️⃣ Multiple Exception Handling

```python
try:
    data = int(input_value)
except ValueError:
    print("Not a number")
except TypeError:
    print("Invalid type")
```

Why this matters:

* API responses
* User input
* Config parsing

---

## 4️⃣ finally — Cleanup Always Runs

```python
try:
    f = open("file.txt")
    process(f)
except Exception as e:
    print(e)
finally:
    f.close()
```

Used for:

* Closing files
* Releasing locks
* Cleanup before exit

---

## 5️⃣ Raising Your Own Exceptions (CRITICAL SKILL)

If something is wrong, **say it explicitly**.

```python
def validate_env(env):
    if env not in ("dev", "prod"):
        raise ValueError(f"Invalid environment: {env}")
```

This prevents:

* Bad deployments
* Wrong environment actions

---

## 6️⃣ Custom Exceptions (For Clarity)

```python
class ConfigError(Exception):
    pass
```

Usage:

```python
if "env" not in config:
    raise ConfigError("Missing env in config")
```

Your future self will thank you.

---

## 7️⃣ Exit Codes — THIS IS HOW DEVOPS TOOLS TALK

### Exit codes you MUST know

| Code | Meaning            |
| ---- | ------------------ |
| 0    | Success            |
| 1    | General failure    |
| 2    | Misuse / bad input |

---

### Use `sys.exit()`

```python
import sys

if error:
    sys.exit(1)

sys.exit(0)
```

CI/CD systems rely on this.

---

## 8️⃣ Combining Exceptions + Exit Codes (REAL PATTERN)

```python
import sys

try:
    config = load_config()
except FileNotFoundError:
    print("Config missing")
    sys.exit(1)
except ValueError as e:
    print(e)
    sys.exit(2)

print("Config OK")
sys.exit(0)
```

This is **production-grade behavior**.

---

## 9️⃣ DO NOT Catch Everything

### ❌ WRONG

```python
except Exception:
    print("Something went wrong")
```

Why it’s bad:

* No context
* No action
* Debug nightmare

Only catch what you can **handle or explain**.

---

## 10️⃣ Common DevOps Failure Scenarios

You MUST expect failures in:

* Missing config files
* Bad JSON / YAML
* API timeouts
* Permission denied
* Network unreachable

If your script assumes success → it’s broken.

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Safe Config Loader

Create `safe_config.py`:

* Read `config.json`
* If file missing → print message → exit 1
* If `env` missing → exit 2
* If all good → print “Config OK” → exit 0

---

### 📝 Assignment 2 — Environment Validator

Write a function:

```python
def validate_env(env):
    ...
```

Rules:

* Allowed: `dev`, `stage`, `prod`
* Invalid → raise `ValueError`
* Caller handles exception and exits properly

---

### 📝 Assignment 3 — Fail Loudly

Create a script that:

* Accepts a filename
* Tries to read it
* On success → exit 0
* On failure → print reason → exit 1

---

Perfect set of assignments, Ganesh 👍. Let’s scaffold each one step by step in Python, keeping them modular and easy to reuse.  

---

### 📝 Assignment 1 — Safe Config Loader (`safe_config.py`)

```python
import json
import sys
import os

def main():
    config_file = "config.json"

    # Check if file exists
    if not os.path.exists(config_file):
        print("Config file missing")
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)

    # Check for 'env' key
    env = config.get("env")
    if not env:
        print("Environment missing in config")
        sys.exit(2)

    print("Config OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 2 — Environment Validator

```python
def validate_env(env: str) -> None:
    allowed = {"dev", "stage", "prod"}
    if env not in allowed:
        raise ValueError(f"Invalid environment: {env}")
```

**Usage Example:**

```python
import sys

try:
    validate_env("test")  # invalid
except ValueError as e:
    print(e)
    sys.exit(2)
```

---

### 📝 Assignment 3 — Fail Loudly

```python
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fail_loudly.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            _ = f.read()
        sys.exit(0)
    except Exception as e:
        print(f"Failed to read file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

✅ These scripts follow your rules:
- Exit codes are explicit (`0`, `1`, `2`).  
- Errors are printed clearly.  
- Environment validation is strict and reusable.  

## ✅ Chapter 4 Exit Criteria (STRICT)

You move on ONLY if:

* You don’t use bare `except`
* You raise exceptions intentionally
* You exit with meaningful codes
* You understand that **crashing is sometimes correct**

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 5 — OS & System Interaction (`os`, `sys`, `shutil`)**

Reply with:

1. Your code for all 3 assignments
2. Exit codes you observed
3. One sentence: *why silent failure is worse than crashing*

No rushing.
Do it right — or we fix it.
