# 📘 CHAPTER 2 — Python Syntax for DevOps (DEEP, PRACTICAL)

This is NOT “learn Python”.
This is **learn to write automation that doesn’t break production**.


## 🎯 Chapter 2 Goal

By the end of this chapter, you must be able to:

* Model real infra data using Python types
* Write safe condition logic
* Loop without creating bugs
* Write functions that don’t surprise callers

If you already “know Python”, prove it by writing **clean automation-style code**.

---

## 1️⃣ Data Types That Actually Matter in DevOps

Forget theory. These four matter **90% of the time**:

### ✅ `str`

Used for:

* Paths
* Commands
* Hostnames
* IDs

```python
service = "nginx"
env = "prod"
```

---

### ✅ `int` / `float`

Used for:

* Ports
* Thresholds
* Counts
* Timeouts

```python
port = 8080
timeout = 5.5
```

---

### ✅ `list`

Used for:

* Servers
* Files
* Containers
* Pods

```python
servers = ["app1", "app2", "app3"]
```

---

### ✅ `dict` (MOST IMPORTANT)

Used for:

* Configs
* API responses
* Metadata

```python
server = {
    "name": "app1",
    "ip": "10.0.0.1",
    "status": "running"
}
```

📌 If you don’t master `dict`, stop pretending to do DevOps automation.

---

## 2️⃣ Reading & Accessing Data Safely

### ❌ Wrong (will crash)

```python
print(server["cpu"])
```

### ✅ Correct (safe)

```python
cpu = server.get("cpu", "unknown")
print(cpu)
```

Production automation **must not crash** because a key is missing.

---

## 3️⃣ Conditions — Control Without Chaos

### Basic condition

```python
if server["status"] == "running":
    print("OK")
else:
    print("NOT OK")
```

### Multiple conditions

```python
if status == "running" and env == "prod":
    print("Monitor aggressively")
```

### Membership check (VERY common)

```python
if "app1" in servers:
    print("Target found")
```

---

## 4️⃣ Loops — Automation Core

### Loop through servers

```python
for server in servers:
    print(server)
```

### Loop with index (rare but useful)

```python
for i, server in enumerate(servers):
    print(i, server)
```

### Loop through dict (API style)

```python
for key, value in server.items():
    print(key, value)
```

---

## 5️⃣ Functions — THIS IS WHERE PEOPLE FAIL

### ❌ Bad function (unpredictable)

```python
def check():
    print("checking")
```

### ✅ Good function (DevOps-grade)

```python
def check_service(name: str, status: str) -> bool:
    return status == "running"
```

Why this matters:

* Inputs are clear
* Output is predictable
* Testable
* Reusable

---

## 6️⃣ Default Arguments (Used Everywhere)

```python
def restart_service(name, force=False):
    if force:
        print("Force restart")
    else:
        print("Graceful restart")
```

Used in:

* CLI tools
* CI helpers
* Automation flags

---

## 7️⃣ Common DevOps Syntax Mistakes (STOP DOING THESE)

| Mistake          | Why it’s bad                 |
| ---------------- | ---------------------------- |
| Deep nested `if` | Unmaintainable               |
| No functions     | Impossible to test           |
| Global variables | Hidden bugs                  |
| Hardcoded values | Environment-specific failure |

---

# 🧠 ASSIGNMENTS (NO SKIPPING)

### 📝 Assignment 1 — Server Status Checker

Create `status_check.py`:

Input:

```python
servers = [
    {"name": "app1", "status": "running"},
    {"name": "app2", "status": "stopped"},
]
```

Output:

```
app1 -> OK
app2 -> NOT OK
```

---

### 📝 Assignment 2 — Safe Config Reader

Given:

```python
config = {
    "env": "prod",
    "timeout": 30
}
```

Print:

* env
* timeout
* retries (default = 3 if missing)

---

### 📝 Assignment 3 — Function Discipline

Write a function:

```python
def should_alert(env, status):
    ...
```

Rules:

* Alert only if `env == "prod"` AND `status != "running"`
* Return `True` or `False`
* NO prints inside function

---

## ✅ Chapter 2 Exit Criteria (STRICT)

You move on ONLY if:

* You complete all 3 assignments
* You don’t use global variables
* Your functions return values (not prints)
* Code runs without modification

---

Alright Ganesh, let’s tackle these three assignments one by one with clean, reproducible Python code.  

---

## 📝 Assignment 1 — Server Status Checker

**status_check.py**

```python
servers = [
    {"name": "app1", "status": "running"},
    {"name": "app2", "status": "stopped"},
]

for server in servers:
    if server["status"] == "running":
        print(f"{server['name']} -> OK")
    else:
        print(f"{server['name']} -> NOT OK")
```

👉 Output:
```
app1 -> OK
app2 -> NOT OK
```

---

## 📝 Assignment 2 — Safe Config Reader

```python
config = {
    "env": "prod",
    "timeout": 30
}

# Use dict.get() with default for retries
env = config.get("env")
timeout = config.get("timeout")
retries = config.get("retries", 3)

print("env:", env)
print("timeout:", timeout)
print("retries:", retries)
```

👉 Output:
```
env: prod
timeout: 30
retries: 3
```

---

## 📝 Assignment 3 — Function Discipline

```python
def should_alert(env, status):
    """
    Returns True if alert condition is met:
    - env == "prod"
    - status != "running"
    Otherwise returns False.
    """
    return env == "prod" and status != "running"


# Example usage (no prints inside function, only outside):
print(should_alert("prod", "stopped"))   # True
print(should_alert("prod", "running"))   # False
print(should_alert("dev", "stopped"))    # False
```

👉 Output:
```
True
False
False
```

---

✨ These three scripts together give you:
- A **status checker** for servers.
- A **safe config reader** with defaults.
- A **disciplined function** that returns a boolean without side effects.


## Next Chapter (LOCKED)

➡ **Chapter 3 — Strings, Files & Paths (Real Config & Log Handling)**

Reply with:

1. Your completed code (paste it)
2. Any errors (raw)
3. Confirmation you understand **why dict + functions dominate DevOps Python**

No excuses.
Do the work — then we advance.
