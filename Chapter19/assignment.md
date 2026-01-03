Good. This chapter is about **signal vs noise**, so I’ll give you **production-grade solutions** plus **why each design choice exists**.
These scripts are **Nagios/cron/CI compatible** and intentionally boring. That’s a compliment.

---

# ✅ CHAPTER 19 — Monitoring & Alerting

**Solutions + Explanations (No BS)**

---

## 📁 Recommended Structure

```
chapter19/
├── disk_check.py
├── memory_check.py
├── process_check.py
└── health_check.py
```

All scripts:

* use **logging**
* return **meaningful exit codes**
* never print
* never alert without context

---

## 🔧 Shared Conventions (IMPORTANT)

Exit codes (industry-standard):

* `0` → OK / WARN (non-fatal)
* `2` → CRITICAL (human intervention)

Why?

* cron / CI / schedulers act on exit codes
* WARN is *information*
* CRITICAL is *action*

---

## 📝 Assignment 1 — Disk Health Script

### `disk_check.py`

```python
import shutil
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

WARN_THRESHOLD = 75
CRIT_THRESHOLD = 85

def main():
    total, used, free = shutil.disk_usage("/")
    usage_pct = (used / total) * 100

    if usage_pct >= CRIT_THRESHOLD:
        logger.error("Disk CRITICAL: %.1f%% used", usage_pct)
        sys.exit(2)

    if usage_pct >= WARN_THRESHOLD:
        logger.warning("Disk WARNING: %.1f%% used", usage_pct)
        sys.exit(0)

    logger.info("Disk OK: %.1f%% used", usage_pct)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this is correct

* Uses **percent**, not absolute numbers (portable)
* WARN does **not** break pipelines
* CRITICAL **forces attention**
* No guessing, no magic

Alerting on 60% disk is amateur behavior.

---

## 📝 Assignment 2 — Memory Health Script

### `memory_check.py`

```python
import psutil
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

WARN_THRESHOLD = 70
CRIT_THRESHOLD = 85

def main():
    mem_pct = psutil.virtual_memory().percent

    if mem_pct >= CRIT_THRESHOLD:
        logger.error("Memory CRITICAL: %.1f%% used", mem_pct)
        sys.exit(2)

    if mem_pct >= WARN_THRESHOLD:
        logger.warning("Memory WARNING: %.1f%% used", mem_pct)
        sys.exit(0)

    logger.info("Memory OK: %.1f%% used", mem_pct)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this is correct

* Memory spikes happen — WARN ≠ panic
* CRITICAL threshold is high on purpose
* Uses `psutil` → cross-platform, reliable

If you alert every time memory hits 70%, people will mute alerts.

---

## 📝 Assignment 3 — Process Monitor

### `process_check.py`

```python
import sys
import logging
import psutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def is_running(name: str) -> bool:
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == name:
            return True
    return False

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python process_check.py <process-name>")
        sys.exit(2)

    process_name = sys.argv[1]

    if not is_running(process_name):
        logger.error("Process CRITICAL: %s not running", process_name)
        sys.exit(2)

    logger.info("Process OK: %s running", process_name)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this is correct

* Binary signal: running or not
* No partial states
* CRITICAL only when action is required

Monitoring a non-critical process this way would be wrong. Context matters.

---

## 📝 Assignment 4 — Composite Health Check

### `health_check.py`

```python
import sys
import logging
import shutil
import psutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DISK_WARN = 75
DISK_CRIT = 85
MEM_WARN = 70
MEM_CRIT = 85
PROCESS_NAME = "python"  # example

def check_disk():
    total, used, _ = shutil.disk_usage("/")
    pct = (used / total) * 100
    if pct >= DISK_CRIT:
        return "CRIT", f"Disk {pct:.1f}%"
    if pct >= DISK_WARN:
        return "WARN", f"Disk {pct:.1f}%"
    return "OK", f"Disk {pct:.1f}%"

def check_memory():
    pct = psutil.virtual_memory().percent
    if pct >= MEM_CRIT:
        return "CRIT", f"Memory {pct:.1f}%"
    if pct >= MEM_WARN:
        return "WARN", f"Memory {pct:.1f}%"
    return "OK", f"Memory {pct:.1f}%"

def check_process():
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == PROCESS_NAME:
            return "OK", f"Process {PROCESS_NAME} running"
    return "CRIT", f"Process {PROCESS_NAME} not running"

def main():
    checks = [
        check_disk(),
        check_memory(),
        check_process()
    ]

    has_crit = False
    has_warn = False

    for status, msg in checks:
        if status == "CRIT":
            logger.error(msg)
            has_crit = True
        elif status == "WARN":
            logger.warning(msg)
            has_warn = True
        else:
            logger.info(msg)

    if has_crit:
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this design matters

* **CRITICAL dominates everything**
* WARNs do not block execution
* Logs show **full context**
* Exit code reflects **worst condition**

This pattern scales cleanly to 10+ checks.

---

## 🔥 Alerts You SHOULD NOT Trigger (Example)

You intentionally **do not alert** when:

* Disk is 76% (WARN only)
* Memory spikes briefly
* Process restarts automatically

Why?
Because **humans are expensive**. Interrupt them only when needed.

---

## 🧠 Core Monitoring Rule (Memorize This)

> **Monitoring observes.
> Alerting interrupts.
> Interruptions must be rare.**

If you violate this, your alerts will be ignored—and then outages last longer.

---


---

## 📝 Unified Script: `health_toolbox.py`

```python
import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("HealthToolbox")


# --- Assignment 1: Disk Health ---
def check_disk():
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent >= 85:
        logger.critical("Disk usage CRITICAL: %d%%", percent)
        return 2
    elif percent >= 75:
        logger.warning("Disk usage WARN: %d%%", percent)
        return 0
    else:
        logger.info("Disk usage OK: %d%%", percent)
        return 0


# --- Assignment 2: Memory Health ---
def check_memory():
    mem = psutil.virtual_memory()
    percent = mem.percent
    if percent >= 85:
        logger.critical("Memory usage CRITICAL: %d%%", percent)
        return 2
    elif percent >= 70:
        logger.warning("Memory usage WARN: %d%%", percent)
        return 0
    else:
        logger.info("Memory usage OK: %d%%", percent)
        return 0


# --- Assignment 3: Process Monitor ---
def check_process(name):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info("Process '%s' is running", name)
            return 0
    logger.critical("Process '%s' not running", name)
    return 2


# --- Assignment 4: Composite Health ---
def composite(process_name):
    results = [check_disk(), check_memory(), check_process(process_name)]

    if 2 in results:
        logger.critical("Composite check: CRITICAL failure detected")
        return 2
    elif any(r == 0 for r in results):
        logger.warning("Composite check: WARN detected")
        return 0
    else:
        logger.info("Composite check: All OK")
        return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: health_toolbox.py [disk|memory|process <name>|composite <name>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "disk":
        sys.exit(check_disk())
    elif cmd == "memory":
        sys.exit(check_memory())
    elif cmd == "process":
        if len(sys.argv) < 3:
            logger.error("Missing process name argument")
            sys.exit(2)
        sys.exit(check_process(sys.argv[2]))
    elif cmd == "composite":
        if len(sys.argv) < 3:
            logger.error("Missing process name argument")
            sys.exit(2)
        sys.exit(composite(sys.argv[2]))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

## 🚀 Step‑Wise Execution

### 1. Disk Health
```bash
python health_toolbox.py disk
```
Logs OK/WARN/CRITICAL depending on usage.

### 2. Memory Health
```bash
python health_toolbox.py memory
```

### 3. Process Monitor
```bash
python health_toolbox.py process python
```
Checks if `python` process is running.

### 4. Composite Health
```bash
python health_toolbox.py composite python
```
Runs disk, memory, and process checks together:
- Any CRITICAL → exit 2  
- Any WARN → exit 0 with warnings logged  
- All OK → exit 0  

---

✅ Now you’ve got a **single health toolbox** that handles disk, memory, process, and composite checks — all with proper logging and exit codes.  

## ✅ Chapter 19 — FINAL VERDICT

You now understand:

* How to convert metrics → decisions
* Why WARN ≠ CRITICAL
* Why exit codes matter more than dashboards
* Why alert fatigue is a real failure mode

This is **real DevOps monitoring**, not toy scripts.

---

## 🚀 NEXT CHAPTER

➡ **Chapter 20 — Reliability Patterns**
**(Retries · Timeouts · Idempotency · Failure Tolerance)**

This is where automation survives **bad networks and bad days**.

When ready, say:
