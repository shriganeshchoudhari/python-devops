# 🚀 MOVING ON

## 📘 CHAPTER 10 — Linux Automation with Python

**(Processes · Disk · Memory · Health Checks)**

This is where Python starts touching **real infrastructure**.

---

![Image](https://images.ctfassets.net/o7xu9whrs0u9/yGtSCjGQONVHi7EULTt4I/cefbafff450eef115dabb808fece08bf/linux-system-monitoring-dashboard.png)

![Image](https://www.jeffgeerling.com/sites/default/files/images/btop.jpg)

![Image](https://www.tecmint.com/wp-content/uploads/2021/08/Show-Disk-Usage-in-Human-Readable.png)

![Image](https://images.contentstack.io/v3/assets/blt28ff6c4a2cf43126/blt44823404833e9ffd/65083c8ba07450002c361f67/Hybrid_DNS_Monitoring_and_Troubleshooting_Tool_3_Features_Array_Item_-_features_item_image.png?auto=webp\&disable=upscale\&quality=75\&width=3840)

---

## 🎯 Chapter 10 Goal

By the end of this chapter, you must be able to:

* Inspect running processes
* Check disk usage
* Monitor memory
* Build **health-check scripts** that ops teams actually use

If you can’t observe the system, you can’t automate it.

---

## 1️⃣ Getting System Information

### Platform & OS

```python
import platform

print(platform.system())
print(platform.release())
```

This matters when scripts behave differently on Linux vs Windows.

---

## 2️⃣ Process Inspection (CORE DEVOPS SKILL)

### Using `subprocess` (portable)

```python
import subprocess

result = subprocess.run(
    ["tasklist"] if platform.system() == "Windows" else ["ps", "aux"],
    capture_output=True,
    text=True
)
```

You already know how to handle output — now use it meaningfully.

---

## 3️⃣ Disk Usage (CRITICAL)

```python
import shutil

total, used, free = shutil.disk_usage("/")
```

Convert to percent:

```python
usage_pct = used / total * 100
```

This is how **disk alerts** are born.

---

## 4️⃣ Memory Usage (Cross-Platform)

```python
import psutil
```

Install:

```bash
pip install psutil
```

Usage:

```python
import psutil

mem = psutil.virtual_memory()
print(mem.percent)
```

If you don’t know `psutil`, you are **handicapped** in DevOps Python.

---

## 5️⃣ Process Health Check (REAL PATTERN)

```python
import psutil

def is_process_running(name: str) -> bool:
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == name:
            return True
    return False
```

This replaces fragile shell pipelines.

---

## 6️⃣ Combine Everything — Server Health Script

A real DevOps script checks:

* disk > threshold
* memory > threshold
* critical processes running

And **fails loudly** if unhealthy.

---

## 🧠 ASSIGNMENTS — Chapter 10 (MANDATORY)

### 📝 Assignment 1 — Disk Monitor

* Check disk usage
* If usage > 80% → log ERROR → exit 1
* Else → INFO → exit 0

---

### 📝 Assignment 2 — Memory Monitor

* Use `psutil`
* Log memory percentage
* Threshold = 75%

---

### 📝 Assignment 3 — Process Checker

* Check if a process name exists
* Return True / False
* Log result

---

### 📝 Assignment 4 — Health Check Script

Combine all above:

* If **any** check fails → exit 1
* Log everything
* NO prints

---
Alright Ganesh 👍, let’s build out Chapter 10’s monitoring assignments step by step. We’ll use **`psutil`** for system stats and logging for output (no `print()` at all).  

---

### 📝 Assignment 1 — Disk Monitor (`disk_monitor.py`)
```python
import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DiskMonitor")

def main():
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent > 80:
        logger.error(f"Disk usage high: {percent}%")
        sys.exit(1)
    else:
        logger.info(f"Disk usage OK: {percent}%")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 2 — Memory Monitor (`memory_monitor.py`)
```python
import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MemoryMonitor")

def check_memory(threshold=75):
    mem = psutil.virtual_memory()
    percent = mem.percent
    logger.info(f"Memory usage: {percent}%")
    return percent <= threshold

if __name__ == "__main__":
    ok = check_memory()
    exit(0 if ok else 1)
```

---

### 📝 Assignment 3 — Process Checker (`process_checker.py`)
```python
import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ProcessChecker")

def process_exists(name: str) -> bool:
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info(f"Process '{name}' is running")
            return True
    logger.error(f"Process '{name}' not found")
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logger.error("Missing process name argument")
        sys.exit(1)
    exists = process_exists(sys.argv[1])
    sys.exit(0 if exists else 1)
```

---

### 📝 Assignment 4 — Health Check Script (`health_check.py`)
Combine all checks: disk, memory, process. If any fails → exit 1.  

```python
import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("HealthCheck")

def check_disk(threshold=80):
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent > threshold:
        logger.error(f"Disk usage high: {percent}%")
        return False
    logger.info(f"Disk usage OK: {percent}%")
    return True

def check_memory(threshold=75):
    mem = psutil.virtual_memory()
    percent = mem.percent
    if percent > threshold:
        logger.error(f"Memory usage high: {percent}%")
        return False
    logger.info(f"Memory usage OK: {percent}%")
    return True

def check_process(name: str):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info(f"Process '{name}' is running")
            return True
    logger.error(f"Process '{name}' not found")
    return False

def main():
    # Example: check disk, memory, and a process (like 'python')
    disk_ok = check_disk()
    mem_ok = check_memory()
    proc_ok = check_process("python")

    if not (disk_ok and mem_ok and proc_ok):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

✅ Summary:
- **Disk Monitor**: Logs usage, exits 1 if >80%.  
- **Memory Monitor**: Logs usage, threshold 75%.  
- **Process Checker**: Logs whether process exists.  
- **Health Check**: Combines all, exits 1 if any fail.  

## ❗ One Last Reality Check

Up to Chapter 9 → **automation logic**
From Chapter 10 onward → **infrastructure responsibility**

Mistakes here:

* trigger alerts
* restart services
* wake people at night

So slow down and be precise.

---

Reply with:

1. Your Chapter 10 health-check code
2. OS-specific issues you faced (Windows quirks count)
3. One sentence: **why observability comes before automation**

Then we continue to **Chapter 11 — SSH & Remote Execution**.
