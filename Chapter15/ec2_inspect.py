import sys
from aws_client import get_client, logger
from botocore.exceptions import ClientError

def main():
    try:
        ec2 = get_client("ec2")

        response = ec2.describe_instances(
            Filters=[
                {"Name": "instance-state-name", "Values": ["running"]}
            ]
        )

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                tags = {
                    t["Key"]: t["Value"]
                    for t in instance.get("Tags", [])
                }

                logger.info(
                    "InstanceId=%s | State=%s | Tags=%s",
                    instance["InstanceId"],
                    instance["State"]["Name"],
                    tags
                )

        sys.exit(0)

    except ClientError as e:
        logger.error("Failed to inspect EC2 instances: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
