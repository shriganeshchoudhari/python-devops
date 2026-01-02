import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    try:
        client = docker.from_env()
        image, logs = client.images.build(
            path=".",
            tag="myapp:test",
            rm=True
        )
        for chunk in logs:
            if "stream" in chunk:
                logger.info(chunk["stream"].strip())
        logger.info("Image built successfully: myapp:test")
        sys.exit(0)
    except docker.errors.BuildError as e:
        logger.error("Build failed: %s", e)
        sys.exit(1)
    except docker.errors.DockerException as e:
        logger.error("Docker error: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
