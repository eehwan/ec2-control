import click
import sys
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
                click.echo("")
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
            return
    config.create_default_config()
    click.echo(f"Created default config file at {config.CONFIG_PATH}")
