# 📘 CHAPTER 7 — Logging (Why `print()` Is Not Enough)

Logging is **not decoration**.
Logging is how you:

* debug failures at 3 AM
* understand what happened *after* the script is gone
* prove your automation didn’t lie

---

## 🎯 Chapter 7 Goal

By the end of this chapter, you must:

* Replace `print()` with structured logs
* Use log levels correctly
* Write logs to files
* Make logs useful in CI, servers, and containers

If your logs don’t answer **“what happened?”**, they’re useless.

---

## 1️⃣ Why `print()` Is Trash in Production

### ❌ Problems with `print()`

* No severity (info? error? warning?)
* No timestamps
* No easy redirection
* Impossible to filter in CI

```python
print("Something failed")
```

That tells me **nothing**.

---

## 2️⃣ `logging` Module — The Right Tool

### Minimal setup

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Application started")
```

This already beats `print()`.

---

## 3️⃣ Log Levels (MEMORIZE THESE)

| Level    | When to use         |
| -------- | ------------------- |
| DEBUG    | Internal details    |
| INFO     | Normal operation    |
| WARNING  | Something odd       |
| ERROR    | Operation failed    |
| CRITICAL | App cannot continue |

### Example

```python
logging.debug("Config loaded")
logging.info("Service started")
logging.warning("Disk usage high")
logging.error("API call failed")
logging.critical("System unusable")
```

📌 **Rule:**
CI usually runs at `INFO`.
Local debugging runs at `DEBUG`.

---

## 4️⃣ Proper Logger (NOT basicConfig everywhere)

### Correct pattern

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
```

Why this matters:

* Module-level control
* Reusable libraries
* Cleaner output

---

## 5️⃣ Logging to File (REAL DEVOPS NEED)

```python
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
```

Example output:

```
2025-01-01 10:30:12 INFO Service started
```

This is **machine-readable** and **human-readable**.

---

## 6️⃣ Console + File Logging (COMMON PATTERN)

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.FileHandler("app.log")
file.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file)
```

Used in:

* CI pipelines
* Long-running scripts
* Daemons

---

## 7️⃣ Logging Exceptions (MANDATORY)

### ❌ WRONG

```python
except Exception as e:
    print(e)
```

### ✅ CORRECT

```python
except Exception:
    logger.exception("Unexpected failure")
```

This logs:

* Error message
* Full stack trace

Without stack traces, debugging is guesswork.

---

## 8️⃣ Logging + Exit Codes (Together)

```python
try:
    run_task()
except Exception:
    logger.exception("Task failed")
    exit(1)

logger.info("Task completed successfully")
exit(0)
```

This is **production-grade behavior**.

---

## 9️⃣ Logging in Containers & CI (Reality)

* Logs go to **stdout**
* Aggregators collect them
* Files may disappear

📌 **Rule:**
Always log to console.
File logging is optional and environment-specific.

---

## 10️⃣ Logging Mistakes (STOP THESE)

| Mistake         | Why it’s bad    |
| --------------- | --------------- |
| Using `print()` | No severity     |
| Logging secrets | Security breach |
| Too much DEBUG  | Noise           |
| No context      | Useless logs    |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Replace `print()`

Take any earlier script and:

* Remove all `print()`
* Replace with `logging`
* Use INFO and ERROR properly

---

### 📝 Assignment 2 — File + Console Logger

Write a script that:

* Logs to console
* Logs to `app.log`
* Uses timestamps and levels

---

### 📝 Assignment 3 — Exception Logging

Create a script that:

* Triggers an exception
* Logs it with `logger.exception`
* Exits with code 1

---
Alright Ganesh 👍, let’s tackle these logging-focused assignments step by step.  

---

### 📝 Assignment 1 — Replace `print()` with Logging  
Here’s a refactored version of the earlier **file checker** script using `logging` instead of `print()`:

```python
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    if len(sys.argv) < 2:
        logging.error("Missing filename argument")
        sys.exit(2)

    filename = sys.argv[1]

    if os.path.exists(filename):
        logging.info("FOUND")
        sys.exit(0)
    else:
        logging.error("NOT FOUND")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 2 — File + Console Logger  
This script logs to both **console** and **app.log**, with timestamps and levels:

```python
import logging

# Create logger
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

# Formatter with timestamp and level
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Example usage
logger.info("This goes to console and file")
logger.error("This error is logged everywhere")
```

---

### 📝 Assignment 3 — Exception Logging  
This script deliberately triggers an exception, logs it with `logger.exception`, and exits with code `1`:

```python
import logging
import sys

# Configure logger
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("ExceptionLogger")

def main():
    try:
        # Trigger an exception (division by zero)
        result = 10 / 0
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.exception("An error occurred")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

✅ Summary:
- **Assignment 1**: Replaced `print()` with proper logging levels.  
- **Assignment 2**: Logs to both console and file with timestamps.  
- **Assignment 3**: Demonstrates `logger.exception` for full traceback logging.  

Perfect, Ganesh 👍. Let’s unify all three logging assignments into a single **`logging_toolbox.py`** with subcommands (`check`, `dual-log`, `fail`).  

---

### 📝 Unified Logging Toolbox (`logging_toolbox.py`)

```python
import sys
import os
import logging

# --- Configure base logger ---
logger = logging.getLogger("LoggingToolbox")
logger.setLevel(logging.DEBUG)

# Default console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# --- Assignment 1: File Checker with logging ---
def file_check(filename: str) -> int:
    if not filename:
        logger.error("Missing filename argument")
        return 2
    if os.path.exists(filename):
        logger.info("FOUND")
        return 0
    else:
        logger.error("NOT FOUND")
        return 1


# --- Assignment 2: File + Console Logger ---
def dual_logger_demo() -> int:
    # Add file handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("This message goes to console and app.log")
    logger.error("This error is logged everywhere")
    return 0


# --- Assignment 3: Exception Logging ---
def fail_fast() -> int:
    try:
        # Trigger exception
        result = 10 / 0
        logger.info(f"Result: {result}")
        return 0
    except Exception:
        logger.exception("An error occurred during fail_fast")
        return 1


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python logging_toolbox.py <command> [args...]")
        print("Commands: check <filename>, dual-log, fail")
        sys.exit(2)

    command = sys.argv[1]

    if command == "check":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(file_check(filename))
    elif command == "dual-log":
        sys.exit(dual_logger_demo())
    elif command == "fail":
        sys.exit(fail_fast())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

### 🔑 Usage Examples
- **Check file existence with logging**  
  ```bash
  python logging_toolbox.py check myfile.txt
  ```
- **Log to console + file (`app.log`)**  
  ```bash
  python logging_toolbox.py dual-log
  ```
- **Trigger exception and log traceback**  
  ```bash
  python logging_toolbox.py fail
  ```

---

This way you’ve got **one script** that demonstrates all three logging assignments with proper levels, file + console logging, and exception handling.  

## ✅ Chapter 7 Exit Criteria

You move on ONLY if:

* No `print()` remains
* Logs include timestamps
* Exceptions include stack traces
* Exit codes match log severity

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 8 — HTTP & REST APIs (`requests`)**

Reply with:

1. One script where you replaced `print()` with logging
2. A sample log output
3. One sentence: *why logs matter more than success messages*

No shortcuts.
This chapter separates amateurs from professionals.
