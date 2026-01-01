We move on.

**Chapter 8 is where DevOps stops touching servers directly and starts talking to systems like an adult — via APIs.**
If you don’t understand this chapter, cloud, Kubernetes, CI tools, monitoring… all of it will feel like black magic.

---

![Image](https://media.licdn.com/dms/image/v2/C4D12AQHh6l0xkbhTPg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1622931040032?e=2147483647\&t=KP6s82dMHXyOTcVsNCkKypBjIlQSWYCqI4ucfTrzTJg\&v=beta)

![Image](https://www.researchgate.net/publication/369358390/figure/fig1/AS%3A11431281127810255%401679180216268/HTTP-request-and-response-flow.png)

![Image](https://www.kiwiqa.com/wp-content/uploads/2022/05/How-to-incorporate-automate-testing-in-the-DevOps-lifecycle.jpg)

![Image](https://static-assets.codecademy.com/how-to-create-api-in-python/api-interaction-sequence.png)

# 📘 CHAPTER 8 — HTTP & REST APIs (AUTOMATION REALITY)

This is **not web-dev theory**.
This is how DevOps tools actually communicate.

---

## 🎯 Chapter 8 Goal

By the end of this chapter, you must be able to:

* Call REST APIs using Python
* Understand HTTP methods & status codes
* Send headers & auth tokens
* Handle failures properly (timeouts, bad responses)

If you panic when you see JSON from an API, you’re not DevOps-ready.

---

## 1️⃣ What REST APIs Are (DevOps View)

An API is just:

* a URL
* an HTTP method
* headers
* a response (usually JSON)

That’s it. No mystery.

Example:

```
GET https://api.example.com/servers
```

---

## 2️⃣ HTTP Methods You MUST Know

| Method | Meaning        | DevOps Usage                   |
| ------ | -------------- | ------------------------------ |
| GET    | Read data      | Fetch status, metrics          |
| POST   | Create         | Trigger jobs, create resources |
| PUT    | Replace        | Update configs                 |
| PATCH  | Partial update | Modify settings                |
| DELETE | Remove         | Delete resources               |

If you misuse methods, you automate the **wrong behavior**.

---

## 3️⃣ Status Codes (MEMORIZE THESE)

| Code | Meaning      | What YOU should do |
| ---- | ------------ | ------------------ |
| 200  | OK           | Continue           |
| 201  | Created      | Validate           |
| 400  | Bad request  | Fix input          |
| 401  | Unauthorized | Fix auth           |
| 403  | Forbidden    | Permission issue   |
| 404  | Not found    | Handle gracefully  |
| 500  | Server error | Retry or fail      |

If your script ignores status codes, it lies.

---

## 4️⃣ Using `requests` (THE TOOL)

### Install

```bash
pip install requests
```

### Simple GET

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)
print(response.text)
```

Already more powerful than most shell scripts.

---

## 5️⃣ Parsing JSON (THIS IS DAILY WORK)

```python
data = response.json()
print(data)
```

API responses → **dict + list**
This is why Chapter 2 mattered.

---

## 6️⃣ Headers (VERY IMPORTANT)

Used for:

* Auth tokens
* Content type
* Versioning

```python
headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
```

---

## 7️⃣ Authentication (TOKEN-BASED)

Most DevOps APIs use tokens.

```python
headers = {
    "Authorization": "Bearer MY_TOKEN"
}
```

📌 Rule:

* NEVER hardcode tokens
* Read from environment variables

```python
import os
token = os.getenv("API_TOKEN")
```

If you hardcode secrets, you’re reckless.

---

## 8️⃣ POST Requests (TRIGGERS & CREATION)

```python
payload = {
    "name": "job1",
    "env": "prod"
}

response = requests.post(url, json=payload)
```

Why `json=` matters:

* Sets headers automatically
* Serializes safely

---

## 9️⃣ Error Handling (MANDATORY)

### ❌ WRONG

```python
requests.get(url)
```

### ✅ Correct

```python
response = requests.get(url, timeout=5)

if response.status_code != 200:
    raise RuntimeError(
        f"API failed: {response.status_code}"
    )
```

---

## 10️⃣ Timeouts (NON-NEGOTIABLE)

```python
requests.get(url, timeout=5)
```

Without timeout:

* Script hangs
* CI hangs
* Pipeline blocks

If you omit timeout, that’s a bug.

---

## 11️⃣ Retry Logic (REALITY)

APIs fail. Networks fail. You must expect this.

Simple retry pattern:

```python
for _ in range(3):
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        break
else:
    raise RuntimeError("API unreachable")
```

---

## 12️⃣ Common DevOps API Mistakes

| Mistake               | Why it’s bad       |
| --------------------- | ------------------ |
| No timeout            | Hung pipelines     |
| Ignoring status codes | False success      |
| Hardcoded tokens      | Security breach    |
| Blind JSON access     | Runtime crashes    |
| No retries            | Fragile automation |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Public API Call

Write a script that:

* Calls `https://api.github.com`
* Prints status code
* Prints one field from JSON
* Uses timeout

---

### 📝 Assignment 2 — Status Code Validator

Write a function:

```python
def check_api(url):
    ...
```

Rules:

* GET request
* If status != 200 → raise exception
* If OK → return parsed JSON

---

### 📝 Assignment 3 — Token Safety

* Read token from env variable `API_TOKEN`
* If missing → log error → exit 1
* If present → print “Token loaded”

(No real API call needed)

---

Alright Ganesh 👍, let’s scaffold each assignment in Python with clean, reusable code.  

---

### 📝 Assignment 1 — Public API Call (`api_call.py`)

```python
import requests

def main():
    url = "https://api.github.com"
    try:
        response = requests.get(url, timeout=5)  # timeout in seconds
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            # Print one field from JSON (example: 'current_user_url')
            print("Field current_user_url:", data.get("current_user_url"))
        else:
            print("API call failed")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 2 — Status Code Validator (`api_validator.py`)

```python
import requests

def check_api(url: str):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}")
    return response.json()

# Example usage
if __name__ == "__main__":
    try:
        data = check_api("https://api.github.com")
        print("API OK, got keys:", list(data.keys())[:5])  # show first 5 keys
    except Exception as e:
        print("Error:", e)
```

---

### 📝 Assignment 3 — Token Safety (`token_safety.py`)

```python
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    token = os.environ.get("API_TOKEN")

    if not token:
        logging.error("API_TOKEN missing in environment")
        sys.exit(1)

    logging.info("Token loaded")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

✅ Summary:
- **Assignment 1**: Calls GitHub API, prints status code + one JSON field, uses timeout.  
- **Assignment 2**: Function `check_api(url)` validates status code, raises exception if not 200.  
- **Assignment 3**: Reads token safely from env, logs error if missing, prints confirmation if present.  

Perfect, Ganesh 👍. Let’s unify your three API/token assignments into a single **`api_toolbox.py`** with subcommands (`call`, `validate`, `token`, `help`).  

---

### 📝 Unified API Toolbox (`api_toolbox.py`)

```python
import sys
import os
import logging
import requests

# --- Configure logger ---
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("APIToolbox")


# --- Assignment 1: Public API Call ---
def api_call() -> int:
    url = "https://api.github.com"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Field current_user_url: {data.get('current_user_url')}")
            return 0
        else:
            logger.error("API call failed")
            return 1
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return 1


# --- Assignment 2: Status Code Validator ---
def check_api(url: str):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}")
    return response.json()

def api_validate() -> int:
    try:
        data = check_api("https://api.github.com")
        logger.info("API OK, got keys: %s", list(data.keys())[:5])
        return 0
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return 1


# --- Assignment 3: Token Safety ---
def token_safety() -> int:
    token = os.environ.get("API_TOKEN")
    if not token:
        logger.error("API_TOKEN missing in environment")
        return 1
    logger.info("Token loaded")
    return 0


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Toolbox — Available Commands:

  call       : Call https://api.github.com, print status + one JSON field.
  validate   : Validate API status code (200 OK) and show JSON keys.
  token      : Check API_TOKEN env variable, log error if missing.
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

    if command == "call":
        sys.exit(api_call())
    elif command == "validate":
        sys.exit(api_validate())
    elif command == "token":
        sys.exit(token_safety())
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
- **Call GitHub API**  
  ```bash
  python api_toolbox.py call
  ```
- **Validate API status**  
  ```bash
  python api_toolbox.py validate
  ```
- **Check token safety**  
  ```bash
  python api_toolbox.py token
  ```
- **Show help guide**  
  ```bash
  python api_toolbox.py help
  ```

---

Now you’ve got a **single toolbox script** that covers API calls, validation, and token safety with logging and proper exit codes.  

Perfect, Ganesh 👍. Let’s extend your **`api_toolbox.py`** so it logs to both **console (with colors)** and a **file (`api.log`)**. This way you’ll have real‑time colored feedback on Windows plus persistent logs for later review.

---

### 📝 Final `api_toolbox.py` with Console + File Logging

```python
import sys
import os
import logging
import requests
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: Fore.GREEN,
        logging.ERROR: Fore.RED,
        logging.WARNING: Fore.YELLOW,
        logging.DEBUG: Fore.CYAN,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

# --- Configure logger ---
logger = logging.getLogger("APIToolbox")
logger.setLevel(logging.DEBUG)

# Console handler with colors
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = ColorFormatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# File handler (no colors, full logs)
file_handler = logging.FileHandler("api.log")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# --- Assignment 1: Public API Call ---
def api_call() -> int:
    url = "https://api.github.com"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Field current_user_url: {data.get('current_user_url')}")
            return 0
        else:
            logger.error("API call failed")
            return 1
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return 1


# --- Assignment 2: Status Code Validator ---
def check_api(url: str):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}")
    return response.json()

def api_validate() -> int:
    try:
        data = check_api("https://api.github.com")
        logger.info("API OK, got keys: %s", list(data.keys())[:5])
        return 0
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return 1


# --- Assignment 3: Token Safety ---
def token_safety() -> int:
    token = os.environ.get("API_TOKEN")
    if not token:
        logger.error("API_TOKEN missing in environment")
        return 1
    logger.info("Token loaded")
    return 0


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Toolbox — Available Commands:

  call       : Call https://api.github.com, print status + one JSON field.
  validate   : Validate API status code (200 OK) and show JSON keys.
  token      : Check API_TOKEN env variable, log error if missing.
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

    if command == "call":
        sys.exit(api_call())
    elif command == "validate":
        sys.exit(api_validate())
    elif command == "token":
        sys.exit(token_safety())
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
- **Call GitHub API**  
  ```bash
  python api_toolbox.py call
  ```
- **Validate API status**  
  ```bash
  python api_toolbox.py validate
  ```
- **Check token safety**  
  ```bash
  python api_toolbox.py token
  ```
- **Show help guide**  
  ```bash
  python api_toolbox.py help
  ```

---

Now you’ll see **colored logs in your Windows console** and a full persistent log in `api.log`.  


## ✅ Chapter 8 Exit Criteria

You move on ONLY if:

* You always use timeout
* You check status codes
* You parse JSON safely
* You never hardcode secrets

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 9 — Advanced API Automation (Pagination, Retries, Rate Limits)**

Reply with:

1. Your code for all 3 assignments
2. One real status code you observed
3. One sentence: *why timeout is mandatory*

No rushing.
APIs are the backbone of modern DevOps — get this right.
