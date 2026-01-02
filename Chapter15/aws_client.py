import logging
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_client(service: str):
    try:
        return boto3.client(service)
    except ClientError as e:
        logger.error("Failed to create %s client: %s", service, e)
        raise
