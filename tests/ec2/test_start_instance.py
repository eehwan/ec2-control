import pytest
from ec2ctl import ec2
from ec2ctl.exceptions import AwsError

def test_start_instance(stopped_instance, ec2_client):
    ec2.start_instance(stopped_instance, "default", "us-east-1")
    assert ec2.get_instance_status(stopped_instance, "default", "us-east-1") == "running"
