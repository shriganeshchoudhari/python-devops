import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        if not containers:
            logger.info("No running containers found")
        for c in containers:
            logger.info("Container: %s | Status: %s", c.name, c.status)
        sys.exit(0)
    except docker.errors.DockerException as e:
        logger.error("Docker unreachable: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
