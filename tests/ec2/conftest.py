import os
import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def ec2_client(aws_credentials):
    with mock_aws():
        yield boto3.client("ec2", region_name="us-east-1")

@pytest.fixture
def running_instance(ec2_client):
    reservation = ec2_client.run_instances(
        ImageId="ami-0abcdef1234567890",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )
    instance_id = reservation["Instances"][0]["InstanceId"]
    ec2_client.get_waiter("instance_running").wait(InstanceIds=[instance_id])
    return instance_id

@pytest.fixture
def stopped_instance(ec2_client):
    reservation = ec2_client.run_instances(
        ImageId="ami-0abcdef1234567890",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )
    instance_id = reservation["Instances"][0]["InstanceId"]
    ec2_client.stop_instances(InstanceIds=[instance_id])
    ec2_client.get_waiter("instance_stopped").wait(InstanceIds=[instance_id])
    return instance_id
