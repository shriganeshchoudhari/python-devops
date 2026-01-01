Alright. **Chapter 9.**
This is where most “Python-for-DevOps” learners fall apart because APIs stop being clean and start being **hostile**.

---

![Image](https://media.geeksforgeeks.org/wp-content/uploads/20220309113947/SpringRESTPagination.png)

![Image](https://files.readme.io/4ce8243-response-headers.png)

![Image](https://docs.aws.amazon.com/images/prescriptive-guidance/latest/cloud-design-patterns/images/retry-backoff-1.png)

![Image](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/devops/media/automated-api-deployments-apiops-architecture-diagram.svg)

# 📘 CHAPTER 9 — Advanced API Automation

**(Pagination · Retries · Rate Limits · Resilience)**

If your script works only when the API behaves perfectly, it’s **garbage automation**.

---

## 🎯 Chapter 9 Goal

By the end of this chapter, you must be able to:

* Handle paginated API responses
* Respect rate limits
* Retry intelligently (not blindly)
* Fail cleanly when APIs misbehave

This chapter turns “API calls” into **reliable automation**.

---

## 1️⃣ Pagination — APIs Don’t Return Everything

Most APIs **do NOT** return all data at once.

Typical patterns:

* `?page=1&per_page=50`
* `next` links in headers
* cursors (`next_cursor`)

### Example (page-based)

```python
import requests

page = 1
all_items = []

while True:
    response = requests.get(
        "https://api.example.com/items",
        params={"page": page, "per_page": 50},
        timeout=5
    )
    response.raise_for_status()

    data = response.json()
    if not data:
        break

    all_items.extend(data)
    page += 1
```

**Hard truth:**
If you don’t implement pagination, you are silently losing data.

---

## 2️⃣ Link-Based Pagination (More Common)

Some APIs return a `next` URL.

```python
url = "https://api.example.com/items"

while url:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    payload = response.json()
    items = payload["items"]
    url = payload.get("next")

    process(items)
```

Never assume structure — **inspect the response**.

---

## 3️⃣ Rate Limiting — APIs WILL THROTTLE YOU

APIs don’t care about your script. They protect themselves.

Common headers:

* `X-RateLimit-Remaining`
* `Retry-After`

### Detect rate limit

```python
if response.status_code == 429:
    raise RuntimeError("Rate limited")
```

### Respect `Retry-After`

```python
import time

retry_after = int(response.headers.get("Retry-After", 5))
time.sleep(retry_after)
```

Ignoring rate limits = temporary bans.

---

## 4️⃣ Retries — Do This Like an Adult

### ❌ WRONG

```python
while True:
    requests.get(url)
```

This can DDoS an API.

---

### ✅ Controlled retry with backoff

```python
import time

for attempt in range(3):
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        break
    time.sleep(2 ** attempt)
else:
    raise RuntimeError("API failed after retries")
```

This is **exponential backoff** — memorize it.

---

## 5️⃣ What Should You Retry?

Retry ONLY on:

* 429 (Too Many Requests)
* 5xx (server errors)
* Network timeouts

DO NOT retry on:

* 400 (bad request)
* 401/403 (auth problems)
* 404 (resource doesn’t exist)

Retrying bad input is stupidity.

---

## 6️⃣ Defensive JSON Parsing (MANDATORY)

### ❌ WRONG

```python
items = response.json()["items"]
```

### ✅ SAFE

```python
payload = response.json()
items = payload.get("items", [])
```

APIs change. Your script must survive.

---

## 7️⃣ Timeouts + Retries + Exit Codes (TOGETHER)

```python
import sys
import requests
import time

for attempt in range(3):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        break
    except requests.RequestException as e:
        if attempt == 2:
            print(e)
            sys.exit(1)
        time.sleep(2 ** attempt)

sys.exit(0)
```

This is **CI-safe automation**.

---

## 8️⃣ Real DevOps Use Cases

* Fetch **all** cloud resources
* Pull metrics from monitoring APIs
* Sync users, repos, jobs
* Validate infra state before deployment

If you can’t do this reliably, you’ll always depend on dashboards.

---

## 9️⃣ Common Failures (STOP THESE)

| Mistake                | Consequence      |
| ---------------------- | ---------------- |
| No pagination          | Missing data     |
| No backoff             | API bans         |
| Blind retries          | Infinite loops   |
| No rate-limit handling | Broken pipelines |
| Unsafe JSON access     | Random crashes   |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Pagination Simulator

Simulate pagination using a loop:

* Pretend API returns 3 pages
* Collect all items into one list
* Print total count

(No real API required)

---

### 📝 Assignment 2 — Retry Wrapper

Write a function:

```python
def get_with_retry(url, retries=3):
    ...
```

Rules:

* Uses timeout
* Retries on failure
* Raises error after retries exhausted

---

### 📝 Assignment 3 — Rate Limit Handler

Write code that:

* Detects `429`
* Reads `Retry-After`
* Sleeps
* Retries once

---
Alright Ganesh 👍, let’s scaffold each assignment in Python with clear, reusable examples.  

---

### 📝 Assignment 1 — Pagination Simulator
We’ll simulate an API that returns 3 pages of items, then collect them all into one list.

```python
def pagination_simulator():
    # Pretend API responses
    pages = [
        ["item1", "item2"],
        ["item3", "item4"],
        ["item5"]
    ]

    all_items = []
    for page in pages:
        all_items.extend(page)

    print("Total items collected:", len(all_items))
    print("Items:", all_items)


if __name__ == "__main__":
    pagination_simulator()
```

---

### 📝 Assignment 2 — Retry Wrapper
A function that retries a GET request up to `retries` times, with timeout handling.

```python
import requests
import time

def get_with_retry(url, retries=3, timeout=5):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            last_error = e
            time.sleep(1)  # small delay before retry
    # If all retries exhausted
    raise RuntimeError(f"Failed after {retries} retries") from last_error


if __name__ == "__main__":
    try:
        resp = get_with_retry("https://api.github.com")
        print("Success:", resp.status_code)
    except Exception as e:
        print("Final error:", e)
```

---

### 📝 Assignment 3 — Rate Limit Handler
Detects HTTP 429, reads `Retry-After` header, sleeps, and retries once.

```python
import requests
import time

def rate_limit_handler(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            # Retry once
            response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    resp = rate_limit_handler("https://api.github.com")
    if resp:
        print("Final status:", resp.status_code)
```

---

✅ Summary:
- **Assignment 1**: Simulates pagination with 3 fake pages, collects items, prints total count.  
- **Assignment 2**: Implements retry wrapper with timeout and error handling.  
- **Assignment 3**: Handles rate limit (429), respects `Retry-After`, retries once.  

Perfect, Ganesh 👍. Let’s unify your three assignments (pagination simulator, retry wrapper, rate‑limit handler) into a single **CLI toolbox** with subcommands (`paginate`, `retry`, `ratelimit`, `help`).  

---

### 📝 Unified Toolbox (`api_flow_toolbox.py`)

```python
import sys
import time
import requests
import logging

# --- Configure logger ---
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("APIFlowToolbox")


# --- Assignment 1: Pagination Simulator ---
def paginate() -> int:
    # Pretend API responses (3 pages)
    pages = [
        ["item1", "item2"],
        ["item3", "item4"],
        ["item5"]
    ]
    all_items = []
    for page in pages:
        all_items.extend(page)

    logger.info("Total items collected: %d", len(all_items))
    logger.info("Items: %s", all_items)
    return 0


# --- Assignment 2: Retry Wrapper ---
def get_with_retry(url, retries=3, timeout=5):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning("Attempt %d failed: %s", attempt, e)
            last_error = e
            time.sleep(1)
    raise RuntimeError(f"Failed after {retries} retries") from last_error

def retry_demo() -> int:
    try:
        resp = get_with_retry("https://api.github.com")
        logger.info("Success: %s", resp.status_code)
        return 0
    except Exception as e:
        logger.error("Final error: %s", e)
        return 1


# --- Assignment 3: Rate Limit Handler ---
def rate_limit_handler(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            logger.warning("Rate limited. Retrying after %d seconds...", retry_after)
            time.sleep(retry_after)
            response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error: %s", e)
        return None

def ratelimit_demo() -> int:
    resp = rate_limit_handler("https://httpbin.org/status/429")
    if resp:
        logger.info("Final status: %s", resp.status_code)
        return 0
    return 1


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Flow Toolbox — Available Commands:

  paginate   : Simulate pagination (3 pages), collect items, print total count.
  retry      : Demonstrate retry wrapper with timeout and error handling.
  ratelimit  : Handle 429 Too Many Requests, respect Retry-After, retry once.
  help       : Show this usage guide.

Exit Codes:
  0 : Success
  1 : Error
  2 : Missing arguments / Unknown command
"""
    print(help_text.strip())
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(2)

    command = sys.argv[1]

    if command == "paginate":
        sys.exit(paginate())
    elif command == "retry":
        sys.exit(retry_demo())
    elif command == "ratelimit":
        sys.exit(ratelimit_demo())
    elif command == "help":
        sys.exit(show_help())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

### 🔑 Usage Examples
- **Simulate pagination**  
  ```bash
  python api_flow_toolbox.py paginate
  ```
- **Retry wrapper demo**  
  ```bash
  python api_flow_toolbox.py retry
  ```
- **Rate limit handler demo**  
  ```bash
  python api_flow_toolbox.py ratelimit
  ```
- **Show help guide**  
  ```bash
  python api_flow_toolbox.py help
  ```

---

This way you’ve got one neat toolbox script that demonstrates pagination, retry logic, and rate‑limit handling with proper logging and exit codes.  
Perfect, Ganesh 👍. Let’s extend the **`api_flow_toolbox.py`** so both `retry` and `ratelimit` subcommands accept a `--url` option. That way you can test against different endpoints without editing the script.

---

### 📝 Updated `api_flow_toolbox.py`

```python
import sys
import time
import requests
import logging

# --- Configure logger ---
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("APIFlowToolbox")


# --- Assignment 1: Pagination Simulator ---
def paginate() -> int:
    pages = [
        ["item1", "item2"],
        ["item3", "item4"],
        ["item5"]
    ]
    all_items = []
    for page in pages:
        all_items.extend(page)

    logger.info("Total items collected: %d", len(all_items))
    logger.info("Items: %s", all_items)
    return 0


# --- Assignment 2: Retry Wrapper ---
def get_with_retry(url, retries=3, timeout=5):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning("Attempt %d failed: %s", attempt, e)
            last_error = e
            time.sleep(1)
    raise RuntimeError(f"Failed after {retries} retries") from last_error

def retry_demo(url: str) -> int:
    try:
        resp = get_with_retry(url)
        logger.info("Success: %s", resp.status_code)
        return 0
    except Exception as e:
        logger.error("Final error: %s", e)
        return 1


# --- Assignment 3: Rate Limit Handler ---
def rate_limit_handler(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            logger.warning("Rate limited. Retrying after %d seconds...", retry_after)
            time.sleep(retry_after)
            response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error: %s", e)
        return None

def ratelimit_demo(url: str) -> int:
    resp = rate_limit_handler(url)
    if resp:
        logger.info("Final status: %s", resp.status_code)
        return 0
    return 1


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Flow Toolbox — Available Commands:

  paginate             : Simulate pagination (3 pages), collect items, print total count.
  retry [--url <url>]  : Demonstrate retry wrapper with timeout and error handling.
                         Default: https://api.github.com
  ratelimit [--url <url>] : Handle 429 Too Many Requests, respect Retry-After, retry once.
                            Default: https://httpbin.org/status/429
  help                 : Show this usage guide.

Exit Codes:
  0 : Success
  1 : Error
  2 : Missing arguments / Unknown command
"""
    print(help_text.strip())
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(2)

    command = sys.argv[1]

    if command == "paginate":
        sys.exit(paginate())
    elif command == "retry":
        url = "https://api.github.com"
        if "--url" in sys.argv:
            idx = sys.argv.index("--url")
            if idx + 1 < len(sys.argv):
                url = sys.argv[idx + 1]
        sys.exit(retry_demo(url))
    elif command == "ratelimit":
        url = "https://httpbin.org/status/429"
        if "--url" in sys.argv:
            idx = sys.argv.index("--url")
            if idx + 1 < len(sys.argv):
                url = sys.argv[idx + 1]
        sys.exit(ratelimit_demo(url))
    elif command == "help":
        sys.exit(show_help())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

### 🔑 Usage Examples
- **Simulate pagination**  
  ```bash
  python api_flow_toolbox.py paginate
  ```
- **Retry wrapper with default URL (GitHub)**  
  ```bash
  python api_flow_toolbox.py retry
  ```
- **Retry wrapper with custom URL**  
  ```bash
  python api_flow_toolbox.py retry --url https://httpbin.org/status/500
  ```
- **Rate limit handler with default URL (httpbin 429)**  
  ```bash
  python api_flow_toolbox.py ratelimit
  ```
- **Rate limit handler with custom URL**  
  ```bash
  python api_flow_toolbox.py ratelimit --url https://your-api/endpoint
  ```
- **Show help guide**  
  ```bash
  python api_flow_toolbox.py help
  ```

---

Now you can test against **different endpoints dynamically** without editing the script.  



## ✅ Chapter 9 Exit Criteria

You move on ONLY if:

* You understand pagination patterns
* You retry selectively
* You implement backoff
* You never loop infinitely

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 10 — Linux Automation with Python (Processes, Disk, Memory)**

Reply with:

1. Code for all 3 assignments
2. One sentence: *why blind retries are dangerous*

This chapter is where automation starts touching **real infrastructure**.
