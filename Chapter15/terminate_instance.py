import sys
from aws_client import get_client, logger
from botocore.exceptions import ClientError

def terminate_instance(instance_id: str) -> int:
    ec2 = get_client("ec2")

    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response["Reservations"][0]["Instances"][0]

        tags = {
            t["Key"]: t["Value"]
            for t in instance.get("Tags", [])
        }

        logger.info(
            "Terminating InstanceId=%s | State=%s | Tags=%s",
            instance_id,
            instance["State"]["Name"],
            tags
        )

        ec2.terminate_instances(InstanceIds=[instance_id])

        waiter = ec2.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=[instance_id])

        logger.info("Instance %s terminated successfully", instance_id)
        return 0

    except ClientError as e:
        logger.error("Termination failed: %s", e)
        return 1

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python terminate_instance.py <instance-id>")
        sys.exit(2)

    sys.exit(terminate_instance(sys.argv[1]))

if __name__ == "__main__":
    main()
