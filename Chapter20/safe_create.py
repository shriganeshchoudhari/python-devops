import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated external state
EXISTING_RESOURCES = set()

def resource_exists(resource_id: str) -> bool:
    return resource_id in EXISTING_RESOURCES

def create_resource(resource_id: str):
    # Simulated creation
    EXISTING_RESOURCES.add(resource_id)

def safe_create(resource_id: str):
    if resource_exists(resource_id):
        logger.info(
            "Resource %s already exists — skipping creation",
            resource_id
        )
        return

    logger.info("Creating resource: %s", resource_id)
    create_resource(resource_id)
    logger.info("Resource created: %s", resource_id)

def main():
    safe_create("db-001")
    safe_create("db-001")  # safe repeat

if __name__ == "__main__":
    main()
