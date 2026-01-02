import sys
from aws_client import get_client, logger
from botocore.exceptions import ClientError

def main():
    try:
        sts = get_client("sts")
        identity = sts.get_caller_identity()

        logger.info("AWS Account ID: %s", identity["Account"])
        logger.info("Caller ARN: %s", identity["Arn"])

        sys.exit(0)

    except ClientError as e:
        logger.error("AWS authentication failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
