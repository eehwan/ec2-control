import os
import yaml
import boto3
import click
from . import ec2
from .exceptions import ConfigError, AwsError

CONFIG_DIR = os.path.expanduser("~/.ec2ctl")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

def _get_available_profiles():
    """Returns a list of available AWS profiles."""
    return boto3.Session().available_profiles

def _get_available_regions():
    """Returns a list of available EC2 regions."""
    return boto3.Session().get_available_regions('ec2')

def get_config():
    """Loads the config file."""
    if not os.path.exists(CONFIG_PATH):
        raise ConfigError(f"Config file not found: {CONFIG_PATH}. Please run 'ec2ctl init' to create one.")
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing config file {CONFIG_PATH}: {e}")

def create_config_from_aws():
    """Creates a new config file by fetching details from AWS."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # --- Profile Selection ---
    available_profiles = _get_available_profiles()
    if not available_profiles:
        selected_profile = 'default'
        click.echo("No AWS profiles found. Using 'default'.")
    elif len(available_profiles) == 1:
        selected_profile = available_profiles[0]
        click.echo(f"Using the only available AWS profile: '{selected_profile}'")
    else:
        click.echo("Available AWS profiles:")
        for i, p in enumerate(available_profiles):
            click.echo(f"  [{i + 1}] {p}")
        profile_choice = click.prompt("Select a profile", type=int, default=1)
        selected_profile = available_profiles[profile_choice - 1]

    # --- Region Selection ---
    available_regions = _get_available_regions()
    if not available_regions:
        raise ConfigError("Could not determine available AWS regions.")
    
    click.echo("\nAvailable AWS regions:")
    for i, r in enumerate(available_regions):
        click.echo(f"  [{i + 1}] {r}")
    region_choice = click.prompt("Select a region", type=int, default=available_regions.index('ap-northeast-2') + 1 if 'ap-northeast-2' in available_regions else 1)
    selected_region = available_regions[region_choice - 1]

    # --- Fetch Instances and Build Config ---
    click.echo(f"\nFetching EC2 instances from {selected_region} using profile '{selected_profile}'...")
    try:
        instances = ec2.describe_instances_for_config(selected_profile, selected_region)
    except AwsError as e:
        raise ConfigError(f"Could not fetch EC2 instances: {e}")

    if not instances:
        click.echo("No running or stopped instances found in the selected region.")
        # Create a minimal config
        config_data = {
            'default_profile': selected_profile,
            'default_region': selected_region,
            'instances': {}
        }
    else:
        click.echo(f"Found {len(instances)} instances:")
        instance_config = {}
        for inst in instances:
            click.echo(f"  - {inst['name']} ({inst['id']})")
            instance_config[inst['name']] = {
                'id': inst['id'],
                'ssh_user': 'ec2-user',  # Default, user should change
                'ssh_key_path': f"~/.ssh/{inst['key_name']}.pem" if inst['key_name'] else '~/.ssh/your-key.pem'
            }
        
        config_data = {
            'default_profile': selected_profile,
            'default_region': selected_region,
            'instances': instance_config
        }

    # --- Write Config File ---
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
    
    click.echo()
    click.echo(f"Successfully created config file at {CONFIG_PATH}")
    click.echo("Please review the generated config and adjust ssh_user and ssh_key_path as needed.")
    click.echo(f"You can edit the configuration file at: {CONFIG_PATH}")
