import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def safe_run(image: str, name: str) -> int:
    client = docker.from_env()
    container = None

    try:
        existing = client.containers.list(all=True, filters={"name": name})
        if existing:
            raise RuntimeError(f"Container name already exists: {name}")

        container = client.containers.run(
            image,
            detach=True,
            name=name
        )
        container.wait()
        logs = container.logs().decode()
        logger.info("Logs:\n%s", logs)
        return 0

    except Exception as e:
        logger.error("Safe run failed: %s", e)
        return 1

    finally:
        if container:
            logger.info("Removing container: %s", name)
            container.remove(force=True)

def main():
    exit_code = safe_run("myapp:test", "safe_myapp_run")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
