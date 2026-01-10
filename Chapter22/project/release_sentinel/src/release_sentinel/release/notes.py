import subprocess

def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def get_previous_tag():
    res = _run(["git", "describe", "--tags", "--abbrev=0"])
    return res.stdout.strip() if res.returncode == 0 else None

def generate_notes(version: str) -> str:
    prev = get_previous_tag()
    if prev:
        log = _run([
            "git", "log",
            f"{prev}..HEAD",
            "--pretty=format:- %h %s"
        ]).stdout
    else:
        log = _run([
            "git", "log",
            "--pretty=format:- %h %s"
        ]).stdout

    header = f"## Changes in {version}\n"
    return header + (log.strip() or "- Initial release")
