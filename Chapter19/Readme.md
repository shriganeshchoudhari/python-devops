Good. **Chapter 19.**
This is where automation stops being polite and starts **waking people up**. Bad monitoring is worse than no monitoring—noise kills trust.

---

![Image](https://docs.cloudblue.com/cbc/21.0/Resources/Images/Monitoring-and-Alerting-Solution/Monitoring-Solution-Architecture.png)

![Image](https://www.orangemantra.com/blog/wp-content/uploads/2024/10/Key-Components-of-DevOps-Monitoring-1024x499.png)

![Image](https://docs.sysdig.com/image/multithreshold_bypass2.png)

![Image](https://images.ctfassets.net/zsv3d0ugroxu/22ddrqwcAKKKepI6Wf10th/18d34566eef565ea9e31ae9518ce13a1/Opsgenie___Screenshot___alert_notification_flow)

# 📘 CHAPTER 19 — Python for Monitoring & Alerting

**(Health Checks · Thresholds · Signals, not Noise)**

---

## 🎯 Chapter 19 Goal

By the end of this chapter, you must be able to:

* Collect **signals** (not random metrics)
* Apply **clear thresholds**
* Decide when to **alert vs log**
* Fail with **actionable context**
* Avoid alert storms

If everything alerts, **nothing is urgent**.

---

## 1️⃣ Monitoring vs Alerting (Get This Straight)

* **Monitoring** = observe continuously
* **Alerting** = interrupt humans **only when action is required**

Most juniors alert on *data*. Professionals alert on *decisions*.

---

## 2️⃣ What to Monitor (DevOps-Relevant)

Focus on:

* **Availability** (is it up?)
* **Capacity** (will it fill?)
* **Latency** (is it slow?)
* **Errors** (is it failing?)

Ignore vanity metrics unless they predict failure.

---

## 3️⃣ Signals You’ll Actually Use (Python-Friendly)

* Disk usage %
* Memory usage %
* Process running/not running
* HTTP health endpoint
* Exit codes from checks

You already touched disk/memory earlier—now you **decide**.

---

## 4️⃣ Thresholds (No Guessing)

Bad:

```text
Disk high
```

Good:

```text
WARN at 75%, CRITICAL at 85%
```

Rules:

* **WARN** → log + context
* **CRITICAL** → alert + exit non-zero

---

## 5️⃣ Basic Health Check Pattern (Template)

```python
import sys
import logging

def ok(msg):
    logging.info(msg)
    sys.exit(0)

def warn(msg):
    logging.warning(msg)
    sys.exit(0)

def crit(msg):
    logging.error(msg)
    sys.exit(2)
```

Why:

* Exit codes integrate with schedulers/CI/cron
* Logs explain **why**

---

## 6️⃣ Disk Monitoring (Decision-Based)

```python
import shutil

total, used, free = shutil.disk_usage("/")
usage_pct = used / total * 100
```

Decision logic:

```python
if usage_pct >= 85:
    crit(f"Disk critical: {usage_pct:.1f}%")
elif usage_pct >= 75:
    warn(f"Disk warning: {usage_pct:.1f}%")
else:
    ok(f"Disk OK: {usage_pct:.1f}%")
```

No magic numbers. No ambiguity.

---

## 7️⃣ Memory Monitoring (Cross-Platform)

```python
import psutil

mem = psutil.virtual_memory().percent
```

Same threshold discipline applies.
Never alert on spikes without duration logic (later topic).

---

## 8️⃣ Process Checks (Binary Signal)

```python
import psutil

def is_running(name):
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            return True
    return False
```

Alert only if:

* critical process is **not running**
* AND it’s expected to be running

Context matters.

---

## 9️⃣ HTTP Health Checks (Reality)

```python
import requests

r = requests.get("http://localhost:8080/health", timeout=3)
```

Decide on:

* status code
* response time
* content (optional)

Never alert on **one** failure. Use retries (bounded).

---

## 🔥 Alert Fatigue (How You Lose Trust)

Stop doing this:

* Alert on every WARN
* Alert on transient blips
* Alert without remediation hints

Every alert must answer:

1. What broke?
2. Where?
3. What should I do first?

---

## 10️⃣ Outputs (Where Alerts Go)

Python decides **severity**, not destination.

Destinations (later integration):

* stdout (cron/CI)
* log files
* Slack/Webhook
* Email

Decision first. Transport later.

---

# 🧠 ASSIGNMENTS — CHAPTER 19 (MANDATORY)

### 📝 Assignment 1 — Disk Health Script

* Check disk usage
* WARN ≥ 75%, CRITICAL ≥ 85%
* Log message with percentage
* Exit `0` for OK/WARN, `2` for CRITICAL

---

### 📝 Assignment 2 — Memory Health Script

* Use `psutil`
* WARN ≥ 70%, CRITICAL ≥ 85%
* Same exit code discipline

---

### 📝 Assignment 3 — Process Monitor

* Check for a given process name (CLI arg)
* If not running → CRITICAL
* If running → OK

---

### 📝 Assignment 4 — Composite Health Check

Combine all checks:

* Disk
* Memory
* Process

Rules:

* If **any CRITICAL** → exit 2
* Else if any WARN → exit 0 with warnings logged
* Else → OK

No prints. Logging only.

---

## ✅ Chapter 19 Exit Criteria

You move on ONLY if:

* Alerts are decision-based
* Thresholds are explicit
* Exit codes reflect severity
* You understand **why noise is dangerous**

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 20 — Reliability Patterns (Retries, Timeouts, Idempotency)**

Reply with:

1. Your monitoring scripts
2. One alert you decided **NOT** to trigger (and why)
3. One sentence: **why alert fatigue is worse than downtime**

Then we continue.
