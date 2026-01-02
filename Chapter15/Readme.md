Alright. **Chapter 15.**
Now the gloves come off. This is where **mistakes cost real money**, not just broken pods.

If you automate cloud resources blindly, you’ll:

* leak credentials
* spin resources you forget to delete
* rack up bills you can’t justify

So read this like an adult.

---

![Image](https://docs.aws.amazon.com/images/solutions/latest/data-transfer-hub/images/guidance-arch.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/0%2A8VEaWsDpIvRC1xP1)

![Image](https://jayendrapatil.com/wp-content/uploads/2020/06/ec2_instance_lifecycle.png)

![Image](https://media2.dev.to/dynamic/image/width%3D1280%2Cheight%3D720%2Cfit%3Dcover%2Cgravity%3Dauto%2Cformat%3Dauto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fwjw5ubz0utvamhumf7ma.png)

# 📘 CHAPTER 15 — Cloud Automation with Python (AWS + boto3)

This chapter teaches **cloud control**, not “AWS theory”.

---

## 🎯 Chapter 15 Goal

By the end of this chapter, you must be able to:

* Authenticate to AWS safely
* Use `boto3` to interact with services
* Read state **before** creating resources
* Automate without leaking money or credentials

If you skip safety here, you’re irresponsible.

---

## 0️⃣ Hard Requirements (NO EXCEPTIONS)

Before Python:

* An AWS account
* IAM user or role with **limited permissions**
* AWS CLI configured

Test:

```bash
aws sts get-caller-identity
```

If this fails, stop. Fix credentials first.

---

## 1️⃣ Authentication — How boto3 REALLY Works

Install:

```bash
pip install boto3
```

Basic usage:

```python
import boto3

ec2 = boto3.client("ec2")
```

boto3 automatically checks (in order):

1. Environment variables
2. AWS config files (`~/.aws/credentials`)
3. IAM role (EC2 / EKS)

📌 **Rule:**
Never hardcode AWS keys. Ever.

---

## 2️⃣ Verify Identity (MANDATORY FIRST STEP)

```python
sts = boto3.client("sts")
identity = sts.get_caller_identity()
print(identity["Arn"])
```

If you don’t log **who you are**, you don’t know what you’re touching.

---

## 3️⃣ Reading State — EC2 Example (SAFE START)

### List EC2 instances

```python
ec2 = boto3.client("ec2")

response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(
            instance["InstanceId"],
            instance["State"]["Name"]
        )
```

Reading is cheap. Writing is expensive.

---

## 4️⃣ Filtering (ABSOLUTELY REQUIRED)

```python
ec2.describe_instances(
    Filters=[
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
)
```

Never fetch **everything** if you don’t need it.

---

## 5️⃣ Creating Resources (CONTROLLED, EXPLICIT)

### Launch EC2 (example)

```python
ec2.run_instances(
    ImageId="ami-xxxxxxxx",
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1
)
```

⚠️ **Reality check:**

* This costs money
* This should never be done casually
* Always tag resources

---

## 6️⃣ Tagging (NON-NEGOTIABLE)

```python
TagSpecifications=[
    {
        "ResourceType": "instance",
        "Tags": [
            {"Key": "Project", "Value": "python-devops"},
            {"Key": "Owner", "Value": "automation"}
        ]
    }
]
```

Untagged resources = billing chaos.

---

## 7️⃣ Waiting for State (DON’T ASSUME)

```python
waiter = ec2.get_waiter("instance_running")
waiter.wait(InstanceIds=[instance_id])
```

Same rule as Kubernetes:

> created ≠ ready

---

## 8️⃣ Error Handling (AWS-SPECIFIC)

```python
from botocore.exceptions import ClientError

try:
    ec2.describe_instances()
except ClientError as e:
    print(e.response["Error"]["Code"])
```

AWS errors are verbose for a reason. Use them.

---

## 9️⃣ Cleanup (THIS IS WHERE PEOPLE FAIL)

### Terminate instance

```python
ec2.terminate_instances(InstanceIds=[instance_id])
```

If you don’t automate cleanup:

* bills accumulate
* nobody trusts your scripts

---

## 10️⃣ Services You SHOULD Focus On (FIRST)

Do **not** try to automate everything.

Priority order:

1. EC2 (compute)
2. S3 (storage)
3. IAM (permissions)
4. EKS (later, carefully)

Master these, then expand.

---

## 11️⃣ Deadly Cloud Mistakes (DO NOT COMMIT)

| Mistake        | Consequence          |
| -------------- | -------------------- |
| Admin IAM user | Massive blast radius |
| No tagging     | Billing chaos        |
| No cleanup     | $$$ loss             |
| Hardcoded keys | Security incident    |
| Blind creation | Accidental outages   |

---

# 🧠 ASSIGNMENTS — CHAPTER 15 (MANDATORY)

### 📝 Assignment 1 — Identity Check

* Use STS
* Print/log ARN & account ID
* Exit non-zero if auth fails

---

### 📝 Assignment 2 — EC2 Inspector

* List running EC2 instances
* Log instance ID + state + tags
* No creation

---

### 📝 Assignment 3 — Safe Instance Launcher (DRY RUN FIRST)

* Validate AMI ID
* Use `DryRun=True`
* Catch DryRunOperation
* Do NOT actually launch

---

### 📝 Assignment 4 — Cleanup Guard

Write a function:

```python
def terminate_instance(instance_id):
    ...
```

Rules:

* Confirm instance exists
* Log tags
* Terminate
* Verify termination state

---

## ✅ Chapter 15 Exit Criteria

You move on ONLY if:

* You never hardcode AWS keys
* You verify identity before actions
* You tag resources
* You clean up aggressively
* You understand that **cloud ≠ free**

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 16 — Python in CI/CD (Jenkins, Pipelines, Glue Scripts)**

Reply with:

1. Your boto3 assignment code
2. One AWS error you intentionally handled
3. One sentence: **why cloud automation must be paranoid**

Then we continue.
