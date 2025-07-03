import pytest
from ec2ctl import ec2
from ec2ctl.exceptions import AwsError

def test_get_instance_status(running_instance, stopped_instance, ec2_client):
    assert ec2.get_instance_status(running_instance, "default", "us-east-1") == "running"
    assert ec2.get_instance_status(stopped_instance, "default", "us-east-1") == "stopped"
    assert ec2.get_instance_status("i-00000000000000000", "default", "us-east-1") == "not-found"
