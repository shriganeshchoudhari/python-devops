Alright. **Chapter 18.**
This is where careless DevOps engineers leak credentials and get fired. No drama—just facts.

---

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AAD3IAo2z1Xv8WtPS19iQYA.png)

![Image](https://rajeevpentyala.com/wp-content/uploads/2023/05/image.png)

![Image](https://developer.hashicorp.com/_next/image?q=75\&url=https%3A%2F%2Fcontent.hashicorp.com%2Fapi%2Fassets%3Fproduct%3Dtutorials%26version%3Dmain%26asset%3Dpublic%252Fimg%252Fvault%252Fvault-ra-unseal-1.4.png%26width%3D844%26height%3D272\&w=1920)

![Image](https://www.legitsecurity.com/hubfs/Blog%20A%20Guide%20to%20Securing%20Secrets%20into%20CICD%20Pipelines.png)

# 📘 CHAPTER 18 — Secrets & Security

**(ENV Vars · Files · Vault · Zero-Trust Discipline)**

---

## 🎯 Chapter 18 Goal

By the end of this chapter, you must be able to:

* Handle secrets **without hardcoding**
* Load secrets safely via environment variables
* Understand when files are acceptable (and when they are not)
* Integrate with a secrets manager (Vault-style)
* Avoid leaking secrets in logs, Git, or CI

If you ever commit a secret to Git, that secret is **burned forever**. Rotation is mandatory, apologies are useless.

---

## 1️⃣ What Counts as a Secret (Be Precise)

Secrets include:

* API tokens
* Cloud credentials
* Database passwords
* SSH private keys
* Webhook secrets

**NOT secrets:**

* ports
* URLs without creds
* feature flags

Treating non-secrets like secrets wastes time.
Treating secrets like config ends careers.

---

## 2️⃣ Rule #1 — Never Hardcode (Ever)

### ❌ Wrong

```python
API_KEY = "sk-123456"
```

This will leak. Not *if*—*when*.

---

### ✅ Correct — Environment Variables

```python
import os

api_key = os.getenv("API_KEY")
if not api_key:
    raise RuntimeError("API_KEY not set")
```

This is the **baseline**. Everything else builds on this.

---

## 3️⃣ `.env` Files — Local Only, Never Committed

Used for:

* local development
* NOT CI
* NOT production

### `.env`

```
API_KEY=abc123
DB_PASSWORD=secret
```

### Load with Python

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("DB_PASSWORD")
```

📌 **Rules**

* `.env` → in `.gitignore`
* CI should inject env vars directly
* Production should NEVER rely on `.env`

---

## 4️⃣ CI/CD Secrets (Reality)

CI systems inject secrets as env vars:

* Jenkins credentials
* GitHub Actions secrets
* GitLab CI variables

Python doesn’t care **where** env vars come from.

```python
token = os.getenv("DEPLOY_TOKEN")
if not token:
    sys.exit(1)
```

If this fails in CI → **pipeline must stop**.

---

## 5️⃣ Logging Secrets = Instant Failure

### ❌ Career-ending mistake

```python
logger.info("Token=%s", token)
```

Now it’s in:

* CI logs
* log aggregators
* backups

---

### ✅ Safe logging

```python
logger.info("Token loaded successfully")
```

Or mask:

```python
logger.info("Token starts with %s", token[:4])
```

Even masking should be rare.

---

## 6️⃣ Secrets in Files — Only with Encryption

Plaintext secrets on disk are acceptable ONLY if:

* encrypted
* access-controlled
* rotated

Examples:

* encrypted config files
* OS keychain
* secrets manager

Plain YAML with passwords = **no**.

---

## 7️⃣ Secrets Manager (Industry Standard)

This is where tools like **HashiCorp Vault** come in.

Vault provides:

* central secret storage
* access policies
* dynamic credentials
* audit logs

Python does NOT store secrets—it **fetches them**.

---

## 8️⃣ Vault Access Pattern (Conceptual)

```python
import requests
import os

VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

resp = requests.get(
    f"{VAULT_ADDR}/v1/secret/data/db",
    headers={"X-Vault-Token": VAULT_TOKEN}
)

secret = resp.json()["data"]["data"]["password"]
```

Key ideas:

* Token comes from env
* Secret fetched at runtime
* Nothing stored in code or repo

---

## 9️⃣ Zero-Trust Mindset (CRITICAL)

Assume:

* Code will leak
* Logs will be read
* Access will be abused

Therefore:

* Least privilege
* Short-lived secrets
* Rotation by default
* Fail closed (not open)

---

## 10️⃣ Common Security Mistakes (DO NOT COMMIT THESE)

| Mistake                 | Consequence        |
| ----------------------- | ------------------ |
| Hardcoding secrets      | Guaranteed leak    |
| Committing `.env`       | Immediate rotation |
| Logging secrets         | Incident           |
| Long-lived tokens       | High blast radius  |
| One secret for all envs | Cross-env breach   |

---

# 🧠 ASSIGNMENTS — CHAPTER 18 (MANDATORY)

### 📝 Assignment 1 — Env Secret Loader

Write a script that:

* Reads `API_KEY` from env
* Fails if missing
* Logs success **without printing value**

---

### 📝 Assignment 2 — `.env` Safety

* Load secrets from `.env`
* Prove `.env` is in `.gitignore`
* Script fails if run without `.env`

---

### 📝 Assignment 3 — CI Simulation

* Simulate CI by exporting env var
* Run script successfully
* Unset env var → script fails

---

### 📝 Assignment 4 — Secret Fetch Stub

Write a function:

```python
def fetch_secret():
    ...
```

Rules:

* Reads token from env
* Simulates API fetch (no real Vault needed)
* Never logs secret value

---

## ✅ Chapter 18 Exit Criteria

You move on ONLY if:

* No secrets in code
* No secrets in logs
* Env vars are mandatory
* Failures are immediate and loud

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 19 — Python for Monitoring & Alerting**

This is where scripts start waking people up at night.

Reply with:

1. Your secret-handling scripts
2. One mistake you now understand to be dangerous
3. One sentence: **why secrets must never be trusted to humans**

Then we continue.
