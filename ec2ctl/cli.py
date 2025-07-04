import click
import sys
import subprocess
import os
from click.exceptions import Exit
from . import config
from . import ec2
from .exceptions import ConfigError, AwsError

@click.group()
def cli():
    """A CLI tool to manage EC2 instances."""
    pass

# Common options for profile, region, dry-run, verbose
def common_options(f):
    f = click.option('--profile', help='AWS profile to use.')(f)
    f = click.option('--region', help='AWS region to use.')(f)
    f = click.option('--dry-run', is_flag=True, help='Show what would be done without actually doing it.')(f)
    f = click.option('--verbose', is_flag=True, help='Enable verbose output.')(f)
    return f

# Option for skipping confirmation prompts
def confirmation_option(f):
    f = click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompts.')(f)
    return f

def _get_aws_params(profile, region):
    cfg = config.get_config()
    default_profile = cfg.get('default_profile', 'default')
    default_region = cfg.get('default_region', 'ap-northeast-2')
    
    resolved_profile = profile if profile else default_profile
    resolved_region = region if region else default_region
    return resolved_profile, resolved_region

def _get_instance_details(name, cfg):
    configured_instances = cfg.get('instances', {})
    item = configured_instances.get(name)

    if item is None:
        raise ConfigError(f"Instance or group '{name}' not found in config.")

    instance_id = None
    ssh_user = None
    ssh_key_path = None
    ssh_port = None

    if isinstance(item, dict):
        instance_id = item.get('id')
        ssh_user = item.get('ssh_user')
        ssh_key_path = item.get('ssh_key_path')
        ssh_port = item.get('ssh_port')
    elif isinstance(item, str):
        instance_id = item
    elif isinstance(item, (list, tuple)):
        raise ConfigError(f"'{name}' is a group. The 'connect' command only supports single instances.")
    else:
        raise ConfigError(f"Invalid instance definition for '{name}': {item}")

    if not instance_id:
        raise ConfigError(f"Instance ID not found for '{name}' in config.")

    return instance_id, ssh_user, ssh_key_path, ssh_port

@cli.command()
@click.argument('name')
@common_options
@confirmation_option
def start(name, profile, region, dry_run, verbose, yes):
    """Starts an EC2 instance or group."""
    try:
        resolved_profile, resolved_region = _get_aws_params(profile, region)
        cfg = config.get_config()
        instance_ids = ec2.get_instance_ids_from_names([name], cfg)

        if not instance_ids:
            click.echo(f"No instances found for '{name}' in config.", err=True)
            return

        action_description = f"start {', '.join(instance_ids)}"
        if dry_run:
            click.echo(f"Dry run: Would {action_description} (profile: {resolved_profile}, region: {resolved_region}).")
            return

        if not yes and len(instance_ids) > 1: # Ask for confirmation if multiple instances
            if not click.confirm(f"Are you sure you want to {action_description}?"):
                click.echo("Aborted.")
                return

        for instance_id in instance_ids:
            if verbose:
                click.echo(f"Attempting to start {instance_id} (profile: {resolved_profile}, region: {resolved_region})...")
            else:
                click.echo(f"Starting {instance_id}...")
            ec2.start_instance(instance_id, resolved_profile, resolved_region)
            click.echo(f"Successfully started {instance_id}.")

    except (ConfigError, AwsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('name')
@common_options
@confirmation_option
def stop(name, profile, region, dry_run, verbose, yes):
    """Stops an EC2 instance or group."""
    try:
        resolved_profile, resolved_region = _get_aws_params(profile, region)
        cfg = config.get_config()
        instance_ids = ec2.get_instance_ids_from_names([name], cfg)

        if not instance_ids:
            click.echo(f"No instances found for '{name}' in config.", err=True)
            return

        action_description = f"stop {', '.join(instance_ids)}"
        if dry_run:
            click.echo(f"Dry run: Would {action_description} (profile: {resolved_profile}, region: {resolved_region}).")
            return

        if not yes and len(instance_ids) > 1: # Ask for confirmation if multiple instances
            if not click.confirm(f"Are you sure you want to {action_description}?"):
                click.echo("Aborted.")
                return

        for instance_id in instance_ids:
            if verbose:
                click.echo(f"Attempting to stop {instance_id} (profile: {resolved_profile}, region: {resolved_region})...")
            else:
                click.echo(f"Stopping {instance_id}...")
            ec2.stop_instance(instance_id, resolved_profile, resolved_region)
            click.echo(f"Successfully stopped {instance_id}.")

    except (ConfigError, AwsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('name')
@common_options
def status(name, profile, region, dry_run, verbose): # No 'yes' for status
    """Gets the status of an EC2 instance or group."""
    try:
        resolved_profile, resolved_region = _get_aws_params(profile, region)
        cfg = config.get_config()
        instance_ids = ec2.get_instance_ids_from_names([name], cfg)

        if not instance_ids:
            click.echo(f"No instances found for '{name}' in config.", err=True)
            return

        if dry_run:
            click.echo(f"Dry run: Would get status for {', '.join(instance_ids)} (profile: {resolved_profile}, region: {resolved_region}).")
            return

        for instance_id in instance_ids:
            if verbose:
                click.echo(f"Getting status for {instance_id} (profile: {resolved_profile}, region: {resolved_region})...")
            else:
                click.echo(f"Getting status for {instance_id}...")
            state = ec2.get_instance_status(instance_id, resolved_profile, resolved_region)
            click.echo(f"Instance {instance_id} status: {state}")

    except (ConfigError, AwsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)

@cli.command()
@common_options # list also uses common options, but not confirmation
def list(profile, region, dry_run, verbose): # No 'yes' for list
    """Lists all EC2 instances/groups from config."""
    try:
        # For list, profile/region are not directly used in config.get_config()
        # but can be used for verbose output if needed.
        if verbose:
            resolved_profile, resolved_region = _get_aws_params(profile, region)
            click.echo(f"Listing instances (profile: {resolved_profile}, region: {resolved_region})...")

        cfg = config.get_config()
        instances = cfg.get('instances', {})

        if not instances:
            click.echo("No instances or groups configured in ~/.ec2ctl/config.yaml")
            return

        click.echo("Configured EC2 Instances and Groups:")
        for name, ids in instances.items():
            if ids is None:
                click.echo(f"  {name}: (No instance ID specified)", err=True)
                continue
            if type(ids) is list:
                click.echo(f"  {name} (Group):")
                for instance_id in ids:
                    click.echo(f"    - {instance_id}")
            else:
                click.echo(f"  {name}: {ids}")

    except ConfigError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompts.')
def init(yes):
    """Initializes the config file."""
    if config.os.path.exists(config.CONFIG_PATH):
        if not yes and not click.confirm(f"{config.CONFIG_PATH} already exists. Overwrite?"):
            click.echo("Aborted.")
            sys.exit(0)
    config.create_default_config()
    click.echo(f"Created default config file at {config.CONFIG_PATH}")
    sys.exit(0)

@cli.command()
@click.argument('name')
@click.option('--user', help='SSH user name. Overrides config.')
@click.option('--key', help='Path to SSH private key file. Overrides config.')
@click.option('--port', help='SSH port. Overrides config.')
@click.option('--keep-running', is_flag=True, help='Keep instance running after SSH disconnect.')
@common_options
def connect(name, user, key, port, keep_running, profile, region, dry_run, verbose):
    """Connects to an EC2 instance via SSH, starting it if necessary."""
    try:
        resolved_profile, resolved_region = _get_aws_params(profile, region)
        cfg = config.get_config()
        instance_id, ssh_user_cfg, ssh_key_path_cfg, ssh_port_cfg = _get_instance_details(name, cfg)

        # Determine SSH user and key path
        final_ssh_user = user if user else ssh_user_cfg
        final_ssh_key_path = key if key else ssh_key_path_cfg
        final_ssh_port = port if port else ssh_port_cfg

        if not final_ssh_user:
            raise ConfigError("SSH user not specified in config or via --user option.")
        if not final_ssh_key_path:
            raise ConfigError("SSH key path not specified in config or via --key option.")

        if dry_run:
            click.echo(f"Dry run: Would connect to {instance_id} as {final_ssh_user} with key {final_ssh_key_path} (profile: {resolved_profile}, region: {resolved_region}).")
            if not keep_running:
                click.echo(f"Dry run: Would stop {instance_id} on disconnect.")
            return

        # Start instance (idempotent)
        if verbose:
            click.echo(f"Ensuring {instance_id} is running (profile: {resolved_profile}, region: {resolved_region})...")
        else:
            click.echo(f"Ensuring {instance_id} is running...")
        ec2.start_instance(instance_id, resolved_profile, resolved_region)
        click.echo(f"Instance {instance_id} is running.")

        # Get public IP
        if verbose:
            click.echo(f"Getting public IP for {instance_id}...")
        public_ip = ec2.get_instance_public_ip(instance_id, resolved_profile, resolved_region)
        if not public_ip:
            raise AwsError(f"Could not get public IP for {instance_id}. Instance might not have a public IP.")
        click.echo(f"Connecting to {public_ip}...")

        # Construct SSH command
        ssh_command = [
            "ssh",
            "-i", os.path.expanduser(final_ssh_key_path),
        ]
        if final_ssh_port:
            ssh_command.extend(["-p", str(final_ssh_port)])
        ssh_command.append(f"{final_ssh_user}@{public_ip}")

        if verbose:
            click.echo(f"Executing SSH command: {' '.join(ssh_command)}")

        # Execute SSH command and wait for it to finish
        try:
            subprocess.run(ssh_command, check=True)
        except subprocess.CalledProcessError as e:
            raise AwsError(f"SSH command failed with exit code {e.returncode}.") from e
        except FileNotFoundError:
            raise AwsError("'ssh' command not found. Please ensure OpenSSH client is installed and in your PATH.")

        # Stop instance if --keep-running is not set
        if not keep_running:
            if verbose:
                click.echo(f"SSH session ended. Stopping {instance_id} (profile: {resolved_profile}, region: {resolved_region})...")
            else:
                click.echo(f"SSH session ended. Stopping {instance_id}...")
            ec2.stop_instance(instance_id, resolved_profile, resolved_region)
            click.echo(f"Successfully stopped {instance_id}.")
        else:
            click.echo(f"SSH session ended. Instance {instance_id} kept running as requested.")
        sys.exit(0)

    except (ConfigError, AwsError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)
