import subprocess, logging
log = logging.getLogger("deploy_guard.notes")

def generate_notes(n=10, outfile="RELEASE_NOTES.md"):
    try:
        cmd = ["git", "log", f"-{n}", "--pretty=format:%h %an %s"]
        output = subprocess.check_output(cmd, text=True)
        with open(outfile, "w") as f:
            f.write("# Release Notes\n\n")
            f.write(output)
        log.info("Release notes written to %s", outfile)
        return 0
    except subprocess.CalledProcessError as e:
        log.error("Failed to generate notes: %s", e)
        return 2