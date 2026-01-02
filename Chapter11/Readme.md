Alright. **Chapter 11.**
This is where DevOps stops babysitting one machine and starts **controlling fleets**.

If you screw this up, you:

* leak credentials
* hang deployments
* brick servers remotely

So read carefully.

---

![Image](https://www.jmag-international.com/images/function_tutorial/jft024_en.gif)

![Image](https://miro.medium.com/1%2Aa2QTuYwvROOVBtypS14nmg.png)

![Image](https://miro.medium.com/1%2AJLlLKIBqTOqWNhQXFi5d7A.jpeg)

![Image](https://www.rapidseedbox.com/wp-content/uploads/Setting-up-a-Remote-Server.jpg)

# 📘 CHAPTER 11 — SSH & Remote Execution (REAL INFRA CONTROL)

This chapter is about **remote automation**, not “SSH like a human”.

---

## 🎯 Chapter 11 Goal

By the end of this chapter, you must be able to:

* Connect to remote machines programmatically
* Run commands safely over SSH
* Handle authentication properly
* Collect output, errors, and exit status
* Avoid hanging connections

If your script hangs on SSH, your pipeline is dead.

---

## 1️⃣ The DevOps Rule About SSH

### ❌ Human SSH

```bash
ssh user@server
```

### ✅ Automation SSH

* No prompts
* No passwords typed
* No interactive shells
* Deterministic behavior

Automation **must not wait for humans**.

---

## 2️⃣ Authentication — HARD TRUTH

### ❌ Password-based SSH

* Insecure
* Not automatable
* Often disabled

### ✅ Key-based SSH (ONLY ACCEPTABLE WAY)

```text
~/.ssh/id_rsa
~/.ssh/id_rsa.pub
```

Public key → server
Private key → automation

If you don’t use keys, stop here and fix that first.

---

## 3️⃣ Python Tool of Choice — `paramiko`

Install it:

```bash
pip install paramiko
```

This is the **standard** SSH library in Python.

---

## 4️⃣ Basic SSH Connection (NON-INTERACTIVE)

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(
    hostname="server_ip",
    username="user",
    key_filename="~/.ssh/id_rsa",
    timeout=5
)
```

Key points:

* `timeout` → prevents hanging forever
* No password prompts
* Fully automatable

---

## 5️⃣ Running Remote Commands (THIS IS THE CORE)

```python
stdin, stdout, stderr = client.exec_command("uptime")

output = stdout.read().decode()
error = stderr.read().decode()

print(output)
print(error)
```

What you **must always do**:

* Read stdout
* Read stderr
* Decide based on content / exit status

Ignoring stderr = lying to yourself.

---

## 6️⃣ Exit Status (MOST PEOPLE MISS THIS)

```python
exit_status = stdout.channel.recv_exit_status()

if exit_status != 0:
    raise RuntimeError("Remote command failed")
```

If you don’t check this, your script reports **false success**.

---

## 7️⃣ Running Multiple Commands (SAFE PATTERN)

```python
commands = [
    "hostname",
    "df -h",
    "uptime"
]

for cmd in commands:
    stdin, stdout, stderr = client.exec_command(cmd)
    code = stdout.channel.recv_exit_status()
```

DO NOT open a new connection per command unless required.

---

## 8️⃣ File Transfer — SCP via SFTP

```python
sftp = client.open_sftp()
sftp.get("/var/log/syslog", "syslog_copy")
sftp.put("config.txt", "/tmp/config.txt")
sftp.close()
```

Used for:

* log collection
* config distribution
* artifact movement

---

## 9️⃣ Timeouts & Hanging Commands (CRITICAL)

```python
client.exec_command("sleep 100", timeout=10)
```

Without timeouts:

* scripts hang
* CI agents stall
* pipelines block

Timeouts are **mandatory**.

---

## 10️⃣ Cleaning Up (DO NOT LEAK CONNECTIONS)

```python
client.close()
```

Leaked SSH connections = resource exhaustion.

---

## 11️⃣ Common SSH Automation Mistakes (STOP THESE)

| Mistake                       | Consequence        |
| ----------------------------- | ------------------ |
| Password auth                 | Insecure / blocked |
| No timeout                    | Hung pipelines     |
| Ignoring exit code            | False success      |
| Hardcoded IPs                 | Non-scalable       |
| Logging commands with secrets | Credential leaks   |

---

# 🧠 ASSIGNMENTS — CHAPTER 11 (MANDATORY)

### 📝 Assignment 1 — Remote Uptime Checker

* Connect to a remote host
* Run `uptime`
* Log output
* Exit non-zero if command fails

---

### 📝 Assignment 2 — Disk Check Over SSH

* Run `df -h /`
* Parse output
* Log disk usage
* Exit 1 if usage > threshold

---

### 📝 Assignment 3 — Remote File Fetch

* Download a file using SFTP
* Validate local file exists
* Log success / failure

---

### 📝 Assignment 4 — Safe SSH Wrapper

Write a function:

```python
def run_remote(host, user, command):
    ...
```
Alright Ganesh 👍, Chapter 11 is all about **remote monitoring and safe SSH operations**. We’ll use **Paramiko** (a Python SSH/SFTP library) and `logging` for output. No `print()` anywhere, only logs.  

---

### 📝 Assignment 1 — Remote Uptime Checker
```python
import paramiko
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RemoteUptime")

def remote_uptime(host, user, key_file, timeout=10):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command("uptime")
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            logger.info("Uptime: %s", stdout.read().decode().strip())
            client.close()
            sys.exit(0)
        else:
            logger.error("Failed to run uptime: %s", stderr.read().decode().strip())
            client.close()
            sys.exit(exit_code)
    except Exception as e:
        logger.error("Connection error: %s", e)
        sys.exit(1)
```

---

### 📝 Assignment 2 — Disk Check Over SSH
```python
def remote_disk_check(host, user, key_file, threshold=80, timeout=10):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command("df -h /")
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode().splitlines()

        if exit_code == 0 and len(output) > 1:
            # Parse usage percentage from second line
            usage = output[1].split()[4]  # e.g. "45%"
            percent = int(usage.strip('%'))
            logger.info("Disk usage: %d%%", percent)
            client.close()
            if percent > threshold:
                logger.error("Disk usage above threshold")
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            logger.error("Disk check failed: %s", stderr.read().decode().strip())
            client.close()
            sys.exit(exit_code)
    except Exception as e:
        logger.error("Connection error: %s", e)
        sys.exit(1)
```

---

### 📝 Assignment 3 — Remote File Fetch (SFTP)
```python
import os

def remote_file_fetch(host, user, key_file, remote_path, local_path, timeout=10):
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=user, key_filename=key_file)
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.get(remote_path, local_path)
        sftp.close()
        transport.close()

        if os.path.exists(local_path):
            logger.info("File fetched successfully: %s", local_path)
            return 0
        else:
            logger.error("File fetch failed: %s", local_path)
            return 1
    except Exception as e:
        logger.error("SFTP error: %s", e)
        return 1
```

---

### 📝 Assignment 4 — Safe SSH Wrapper
```python
def run_remote(host, user, command, key_file, timeout=10):
    """
    Safe SSH wrapper:
    - Key-based auth only
    - Timeout enforced
    - Exit code checked
    - Logs everything
    """
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, key_filename=key_file, timeout=timeout)

        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()

        if exit_code == 0:
            logger.info("Command succeeded: %s", stdout.read().decode().strip())
        else:
            logger.error("Command failed (%d): %s", exit_code, stderr.read().decode().strip())

        client.close()
        return exit_code
    except Exception as e:
        logger.error("SSH error: %s", e)
        return 1
```

---

✅ Summary:
- **Assignment 1**: Remote uptime check with exit code logging.  
- **Assignment 2**: Disk usage check via SSH, threshold enforced.  
- **Assignment 3**: SFTP file fetch, validates local file exists.  
- **Assignment 4**: Safe SSH wrapper with key-based auth, timeout, exit code logging.  

---
---

### 🔑 What Assignment 1 Does
- Connects to a remote host via SSH (Paramiko).  
- Runs the command `uptime`.  
- Logs the output.  
- Exits with non‑zero if the command fails.  

---

### 🛠 How to Test It

1. **Prepare a test server**  
   - You need a remote Linux machine (could be a VM, cloud instance, or another PC on your LAN).  
   - Make sure SSH is enabled and accessible.  
   - Ensure you can connect with **key‑based authentication** (no password).  
     ```bash
     ssh -i ~/.ssh/id_rsa user@hostname uptime
     ```
     If this works, your script will too.

2. **Run the script locally**  
   Example:
   ```bash
   python remote_uptime.py
   ```
   (assuming you wrote the function `remote_uptime(host, user, key_file)`).

   Or if you bundled it into a toolbox:
   ```bash
   python ssh_toolbox.py uptime --host myserver.com --user ganesh --key ~/.ssh/id_rsa
   ```

3. **Check logs**  
   - If successful, you’ll see something like:
     ```
     INFO: Uptime:  22:47:01 up 10 days,  3:12,  2 users,  load average: 0.01, 0.05, 0.10
     ```
   - If it fails (wrong host, bad key, command error), you’ll see:
     ```
     ERROR: Connection error: ...
     ```
     and the script will exit with code `1`.

4. **Verify exit code**  
   - On Linux/macOS:
     ```bash
     echo $?
     ```
   - On Windows PowerShell:
     ```powershell
     echo $LASTEXITCODE
     ```
   - `0` means success, non‑zero means failure (as per your assignment rules).

---

### ⚡ Quick Safe Test
If you don’t have a remote server handy, you can:
- Spin up a local Linux VM with SSH enabled.  
- Use `localhost` as the host and your own SSH key.  
- Run the script against it — you’ll still get uptime output.  

---

Rules:

* Key-based auth only
* Timeout required
* Exit code checked
* Logs everything
* No prints

---

## ✅ Chapter 11 Exit Criteria

You move on ONLY if:

* You use key-based SSH
* You never hang on SSH
* You check remote exit codes
* You close connections properly

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 12 — Configs & Templates (YAML + Jinja2)**

This is where SSH meets **real configuration management**.

Reply with:

1. Your SSH automation code
2. Errors you hit (raw)
3. One sentence: *why password-based SSH is unacceptable in automation*

Then we continue.
