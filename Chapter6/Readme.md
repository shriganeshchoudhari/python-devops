# 📘 CHAPTER 6 — Subprocess & Shell Control (REAL COMMAND EXECUTION)

This chapter is about **executing OS commands safely**.
This is where Python replaces:

* bash scripts
* PowerShell hacks
* fragile CI steps

---

## 🎯 Chapter 6 Goal

By the end of this chapter, you must be able to:

* Run shell commands safely
* Capture output and errors
* Detect command failure correctly
* Avoid command-injection stupidity

If you blindly use `os.system`, stop. That’s amateur-level.

---

## 1️⃣ Why `subprocess` Exists

### ❌ WRONG (do not use)

```python
import os
os.system("ls -l")
```

Why this is bad:

* No access to output
* No structured error handling
* Hard to debug
* Security risk

---

## 2️⃣ `subprocess.run()` — The Correct Tool

### Basic command

```python
import subprocess

result = subprocess.run(["ls", "-l"])
```

What you get:

* Exit code
* Execution status
* Control

---

### Capture output (MOST COMMON)

```python
result = subprocess.run(
    ["ls", "-l"],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)
print(result.returncode)
```

This is how:

* CI checks succeed/fail
* Logs are captured
* Decisions are made

---

## 3️⃣ Exit Codes — Again (Because It Matters)

```python
if result.returncode != 0:
    print("Command failed")
```

📌 In DevOps:

* `returncode == 0` → success
* anything else → failure

Never ignore this.

---

## 4️⃣ `check=True` — Fail Fast (USE THIS)

```python
subprocess.run(["ls", "missing"], check=True)
```

What happens:

* Raises `CalledProcessError`
* Script stops immediately

This is GOOD for:

* CI
* Deployment steps
* Critical automation

---

### Handling it properly

```python
try:
    subprocess.run(["ls", "missing"], check=True)
except subprocess.CalledProcessError as e:
    print("Command failed")
    print(e)
```

---

## 5️⃣ Shell vs No Shell (SECURITY CRITICAL)

### ❌ DANGEROUS

```python
subprocess.run("rm -rf /", shell=True)
```

### ✅ SAFE

```python
subprocess.run(["rm", "-rf", "temp"])
```

**Rule:**
Use `shell=True` ONLY if you fully control the input.
User input + shell = security disaster.

---

## 6️⃣ Running Platform-Specific Commands

### Detect OS

```python
import sys

if sys.platform.startswith("win"):
    cmd = ["dir"]
else:
    cmd = ["ls", "-l"]
```

Better approach:

* Avoid OS-specific commands
* Use Python stdlib when possible

---

## 7️⃣ Real DevOps Pattern — Validate Command Availability

```python
import shutil

if not shutil.which("docker"):
    print("Docker not installed")
    exit(1)
```

Never assume tools exist.

---

## 8️⃣ Piping & Chaining (DO THIS CAREFULLY)

### ❌ BAD

```python
subprocess.run("ps aux | grep python", shell=True)
```

### ✅ BETTER

```python
p1 = subprocess.run(["ps", "aux"], capture_output=True, text=True)
if "python" in p1.stdout:
    print("Found python")
```

Yes, it’s more verbose.
It’s also **safe and debuggable**.

---

## 9️⃣ Timeouts (VERY IMPORTANT)

```python
subprocess.run(
    ["sleep", "10"],
    timeout=3
)
```

Why this matters:

* Hung processes
* Stuck CI jobs
* Resource leaks

---

## 10️⃣ Common DevOps Mistakes (STOP THESE)

| Mistake                 | Why it’s dangerous |
| ----------------------- | ------------------ |
| `shell=True` with input | Command injection  |
| Ignoring return codes   | False success      |
| No timeout              | Hung pipelines     |
| Parsing stdout blindly  | Fragile logic      |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — Command Runner

Create `run_cmd.py`:

* Accept command from CLI
* Run it using `subprocess.run`
* Capture stdout & stderr
* Print exit code

⚠️ Do NOT use `shell=True`

---

### 📝 Assignment 2 — Tool Validator

Write a script that:

* Checks if `git` exists
* If missing → print error → exit 1
* If present → print version → exit 0

---

### 📝 Assignment 3 — Fail Fast

Write a script that:

* Runs a command that fails
* Uses `check=True`
* Catches exception
* Prints meaningful error
* Exits with non-zero code

---

Alright Ganesh, let’s scaffold each assignment cleanly in Python. These scripts are small but powerful, and they’ll give you hands-on practice with `subprocess` and error handling.  

---

### 📝 Assignment 1 — Command Runner (`run_cmd.py`)

```python
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_cmd.py <command> [args...]")
        sys.exit(2)

    cmd = sys.argv[1:]  # command and args as list

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print("Exit Code:", result.returncode)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

⚠️ Note: `shell=True` is **not** used — we pass the command as a list.

---

### 📝 Assignment 2 — Tool Validator (`tool_validator.py`)

```python
import subprocess
import sys

def main():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
            sys.exit(0)
        else:
            print("Git not found or error running git")
            sys.exit(1)
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 3 — Fail Fast (`fail_fast.py`)

```python
import subprocess
import sys

def main():
    try:
        # Intentionally run a failing command
        subprocess.run(["false"], check=True)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

✅ Summary:
- **Assignment 1**: Runs any command, captures stdout/stderr, prints exit code.  
- **Assignment 2**: Validates `git` availability, prints version or error.  
- **Assignment 3**: Demonstrates `check=True` fail-fast behavior with clear error reporting.  

Would you like me to **bundle these three into one CLI tool with subcommands** (`run`, `validate`, `fail`) just like we did earlier, so you don’t need separate files?
Perfect, Ganesh 👍. Let’s unify all three assignments into **one CLI tool** with subcommands (`run`, `validate`, `fail`). That way you don’t need separate files.

---

### 📝 Unified CLI Tool (`toolbox_cmd.py`)

```python
import sys
import subprocess

def run_command(cmd: list) -> int:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print("Exit Code:", result.returncode)
        return result.returncode
    except Exception as e:
        print(f"Error running command: {e}")
        return 1

def validate_tool() -> int:
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
            return 0
        else:
            print("Git not found or error running git")
            return 1
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        return 1

def fail_fast() -> int:
    try:
        subprocess.run(["false"], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python toolbox_cmd.py <command> [args...]")
        print("Commands: run <cmd...>, validate, fail")
        sys.exit(2)

    command = sys.argv[1]

    if command == "run":
        if len(sys.argv) < 3:
            print("Missing command to run")
            sys.exit(2)
        sys.exit(run_command(sys.argv[2:]))
    elif command == "validate":
        sys.exit(validate_tool())
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
- **Run any command**  
  ```bash
  python toolbox_cmd.py run ls -l
  ```
- **Validate git installation**  
  ```bash
  python toolbox_cmd.py validate
  ```
- **Demonstrate fail-fast**  
  ```bash
  python toolbox_cmd.py fail
  ```

---

This way you have **one script** with clear subcommands, strict exit codes, and reusable functions.  


## ✅ Chapter 6 Exit Criteria (STRICT)

You move on ONLY if:

* You don’t use `os.system`
* You don’t use `shell=True` casually
* You handle return codes
* You understand why timeouts matter

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 7 — Logging (Why `print()` Is Not Enough)**

Reply with:

1. Your code for all 3 assignments
2. Output you observed
3. One line: *why `shell=True` is dangerous*

No shortcuts.
This chapter is where bad DevOps engineers get exposed.
