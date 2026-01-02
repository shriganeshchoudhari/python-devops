import sys
from aws_client import get_client, logger
from botocore.exceptions import ClientError

AMI_ID = "ami-0b46816ffa1234887"        # PLACEHOLDER
INSTANCE_TYPE = "t3.micro"

def main():
    ec2 = get_client("ec2")

    try:
        ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            DryRun=True
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "DryRunOperation":
            logger.info("Dry run successful — launch permissions verified")
            sys.exit(0)

        logger.error("Dry run failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
