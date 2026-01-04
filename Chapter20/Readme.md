Good. **Chapter 20.**
This is where automation stops assuming the world behaves and starts **surviving failure**. Networks lie. APIs flake. Scripts that don’t plan for this are trash.

---

![Image](https://docs.aws.amazon.com/images/prescriptive-guidance/latest/cloud-design-patterns/images/retry-backoff-1.png)

![Image](https://eda-visuals.boyney.io/assets/visuals/eda/understanding-idempotency.png)

![Image](https://images-www.contentful.com/fo9twyrwpveg/72JNtUP9hjK4XruEOgoydI/3d7352c2a7b6c3accb9b468ac766dd3c/ink__32_.png)

![Image](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2022/06/01/Figure-1.-Resilience-patterns-and-trade-offs.png)

# 📘 CHAPTER 20 — Reliability Patterns

**(Retries · Timeouts · Idempotency · Failure Tolerance)**

---

## 🎯 Chapter 20 Goal

By the end of this chapter, you must be able to:

* Decide **what** to retry and **what not**
* Use **timeouts everywhere**
* Design **idempotent** automation
* Fail fast **without causing damage**
* Prevent duplicate actions under retries

If your script retries blindly, it will eventually break something important.

---

## 1️⃣ The Hard Truth About Failure

Failures are normal:

* DNS hiccups
* TCP resets
* 500s from APIs
* Temporary auth issues

What’s **not** acceptable:

* Infinite retries
* No timeouts
* Duplicate side effects

---

## 2️⃣ Timeouts — Mandatory, Everywhere

### ❌ Wrong

```python
requests.get(url)
```

This can hang forever.

### ✅ Correct

```python
requests.get(url, timeout=5)
```

Rules:

* Pick a timeout
* Make it explicit
* Shorter is usually better

Timeouts are **self-respect for automation**.

---

## 3️⃣ Retries — Be Selective or Don’t Retry

### Retry ONLY on:

* network errors
* timeouts
* HTTP 429
* HTTP 5xx

### NEVER retry on:

* 400 (bad input)
* 401/403 (auth)
* 404 (resource missing)

Retrying these is stupidity, not resilience.

---

## 4️⃣ Exponential Backoff (MEMORIZE)

### ❌ Wrong

```python
while True:
    call_api()
```

### ✅ Correct

```python
import time

for attempt in range(3):
    try:
        call_api()
        break
    except Exception:
        time.sleep(2 ** attempt)
else:
    raise RuntimeError("Failed after retries")
```

Why:

* Reduces load
* Avoids thundering herd
* Respects shared systems

---

## 5️⃣ Circuit Breaker (Conceptual, Critical)

If something keeps failing:

* Stop trying
* Fail fast
* Let systems recover

Blind retries amplify outages.

Simple pattern:

```python
failures = 0
if failures > 3:
    raise RuntimeError("Circuit open")
```

Not fancy. Very effective.

---

## 6️⃣ Idempotency — The Most Important Concept Here

**Idempotent** means:

> Running the same operation twice has the same effect as once.

### ❌ Non-idempotent

```python
create_user("alice")
create_user("alice")  # duplicate
```

### ✅ Idempotent

```python
if not user_exists("alice"):
    create_user("alice")
```

Retries without idempotency = duplicates, leaks, corruption.

---

## 7️⃣ Idempotency Keys (APIs & CI)

Pattern:

```python
headers = {
    "Idempotency-Key": job_id
}
```

If API supports this, **always use it**.

---

## 8️⃣ Safe File Operations (Idempotent by Design)

### ❌ Dangerous

```python
shutil.copy(src, dst)
```

### ✅ Safe

```python
if not Path(dst).exists():
    shutil.copy(src, dst)
```

Now retries won’t overwrite or corrupt.

---

## 9️⃣ Combining It All (REAL PATTERN)

```python
import requests
import time

def fetch(url):
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503):
                raise RuntimeError("Retryable")
            raise RuntimeError("Non-retryable")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
```

This is **reliable automation**, not wishful thinking.

---

## 🔥 Common Reliability Failures (STOP THESE)

| Failure          | Why it’s bad      |
| ---------------- | ----------------- |
| No timeout       | Hung jobs         |
| Infinite retries | Cascading failure |
| Blind retries    | Data corruption   |
| No idempotency   | Duplicates        |
| Retry everything | Masked bugs       |

---

# 🧠 ASSIGNMENTS — CHAPTER 20 (MANDATORY)

### 📝 Assignment 1 — Timeout Wrapper

Write a function that:

* Calls a URL
* Uses timeout
* Fails if timeout exceeded

---

### 📝 Assignment 2 — Retry with Backoff

Write a function:

```python
def get_with_retry(url):
    ...
```

Rules:

* Max 3 attempts
* Exponential backoff
* Retry only on network/5xx
* Raise final error

---

### 📝 Assignment 3 — Idempotent File Creator

* Create a file
* If exists → do nothing
* Safe to run multiple times

---

### 📝 Assignment 4 — Idempotent Action Guard

Write a function:

```python
def safe_create(resource_id):
    ...
```

Rules:

* Check existence first
* Create only if missing
* Log decision
* Safe under retries

---

## ✅ Chapter 20 Exit Criteria

You move on ONLY if:

* Every network call has a timeout
* Retries are bounded and selective
* Idempotency is enforced
* Failures don’t cause damage

---

## Next (FINAL CORE CHAPTER)

➡ **Chapter 21 — Production-Grade Python Projects**

This is where everything you learned becomes:

* structured
* testable
* shippable
