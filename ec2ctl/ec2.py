import boto3
from botocore.exceptions import ClientError
from .exceptions import AwsError, ConfigError

def _get_ec2_client(profile, region):
    """Helper to get an EC2 client with specified profile and region."""
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        return session.client('ec2')
    except Exception as e:
        raise AwsError(f"Failed to create AWS session or client: {e}")

def start_instance(instance_id, profile, region):
    """Starts an EC2 instance."""
    ec2 = _get_ec2_client(profile, region)
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        return True
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'IncorrectInstanceState':
            raise AwsError(f"Instance {instance_id} is already running or in an invalid state for starting.")
        elif error_code == 'UnauthorizedOperation':
            raise AwsError(f"Permission denied to start instance {instance_id}. Check your AWS credentials and IAM policies.")
        elif error_code == 'InvalidInstanceID.NotFound':
            raise AwsError(f"Instance {instance_id} not found.")
        else:
            raise AwsError(f"Failed to start instance {instance_id}: {e}")

def stop_instance(instance_id, profile, region):
    """Stops an EC2 instance."""
    ec2 = _get_ec2_client(profile, region)
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        ec2.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])
        return True
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'IncorrectInstanceState':
            raise AwsError(f"Instance {instance_id} is already stopped or in an invalid state for stopping.")
        elif error_code == 'UnauthorizedOperation':
            raise AwsError(f"Permission denied to stop instance {instance_id}. Check your AWS credentials and IAM policies.")
        elif error_code == 'InvalidInstanceID.NotFound':
            raise AwsError(f"Instance {instance_id} not found.")
        else:
            raise AwsError(f"Failed to stop instance {instance_id}: {e}")

def get_instance_status(instance_id, profile, region):
    """Gets the status of an EC2 instance."""
    ec2 = _get_ec2_client(profile, region)
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        if response['Reservations'] and response['Reservations'][0]['Instances']:
            return response['Reservations'][0]['Instances'][0]['State']['Name']
        return "not-found"
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'InvalidInstanceID.NotFound':
            return "not-found" # Return not-found for consistency
        elif error_code == 'UnauthorizedOperation':
            raise AwsError(f"Permission denied to get status for instance {instance_id}. Check your AWS credentials and IAM policies.")
        else:
            raise AwsError(f"Failed to get status for instance {instance_id}: {e}")

def get_instance_ids_from_names(names, config_data):
    """Resolves instance names/groups to a list of instance IDs."""
    instance_ids = []
    configured_instances = config_data.get('instances', {})

    for name in names:
        ids = configured_instances.get(name)
        if ids is None:
            raise ConfigError(f"Instance or group '{name}' not found in config.")
        
        if isinstance(ids, list):
            instance_ids.extend(ids)
        else:
            instance_ids.append(ids)
    return list(set(instance_ids)) # Return unique IDs
