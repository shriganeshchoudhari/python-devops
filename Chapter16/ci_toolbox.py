import os
import sys
import logging
import re
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CIToolbox")

# --- Assignment 1: CI Validator ---
def validate():
    required_files = ["Dockerfile", "requirements.txt"]
    missing = [f for f in required_files if not os.path.exists(f)]

    if missing:
        for f in missing:
            logger.error("Missing required file: %s", f)
        return 1
    else:
        logger.info("All required files present")
        return 0


# --- Assignment 2: Environment Gate ---
def env_gate():
    env = os.environ.get("ENV")
    allowed = ["dev", "stage", "prod"]

    if env not in allowed:
        logger.error("Invalid ENV value: %s", env)
        return 1
    else:
        logger.info("Environment OK: %s", env)
        return 0


# --- Assignment 3: Version Gate ---
def version_gate(version):
    pattern = r"^v\d+\.\d+\.\d+$"
    if re.match(pattern, version):
        logger.info("Version OK: %s", version)
        return 0
    else:
        logger.error("Invalid version format: %s", version)
        return 1


# --- Assignment 4: Pipeline Simulation ---
def pipeline(version="v1.0.0"):
    logger.info("Starting CI pipeline...")

    if validate() != 0:
        logger.error("Pipeline stopped at validate step")
        return 1

    if env_gate() != 0:
        logger.error("Pipeline stopped at env gate step")
        return 1

    if version_gate(version) != 0:
        logger.error("Pipeline stopped at version gate step")
        return 1

    logger.info("Pipeline completed successfully")
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: ci_toolbox.py [validate|env|version <vX.Y.Z>|pipeline]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "validate":
        sys.exit(validate())
    elif cmd == "env":
        sys.exit(env_gate())
    elif cmd == "version":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(version_gate(sys.argv[2]))
    elif cmd == "pipeline":
        version = sys.argv[2] if len(sys.argv) > 2 else "v1.0.0"
        sys.exit(pipeline(version))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()