import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    client = docker.from_env()
    container = None

    try:
        container = client.containers.run(
            "myapp:test",
            detach=True,
            name="myapp_test_run"
        )
        container.wait()
        logs = container.logs().decode()
        logger.info("Container logs:\n%s", logs)
        sys.exit(0)
    except docker.errors.ContainerError as e:
        logger.error("Container failed: %s", e)
        sys.exit(1)
    finally:
        if container:
            logger.info("Cleaning up container")
            container.remove(force=True)

if __name__ == "__main__":
    main()
