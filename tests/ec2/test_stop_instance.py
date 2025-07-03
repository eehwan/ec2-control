import pytest
from ec2ctl import ec2
from ec2ctl.exceptions import AwsError

def test_stop_instance(running_instance, ec2_client):
    ec2.stop_instance(running_instance, "default", "us-east-1")
    assert ec2.get_instance_status(running_instance, "default", "us-east-1") == "stopped"
