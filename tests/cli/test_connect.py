import pytest
from unittest.mock import patch, MagicMock
import yaml
import os
from ec2ctl import cli
from ec2ctl import config
from ec2ctl.exceptions import AwsError, ConfigError

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

def test_connect_command_default_stop(runner, mock_ec2_functions, prepared_config, mock_subprocess_run):
    mock_get_ids, mock_start, mock_stop, mock_get_status = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_get_status.return_value = "stopped" # Assume it's stopped initially
    mock_start.return_value = True
    mock_subprocess_run.return_value = MagicMock(returncode=0) # SSH exits successfully

    # Mock get_instance_public_ip to return a dummy IP
    with patch('ec2ctl.ec2.get_instance_public_ip', return_value="192.168.1.100") as mock_get_ip:
        result = runner.invoke(cli.cli, ['connect', 'dev-server'])

        assert result.exit_code == 1
        assert "Error: SSH user not specified in config or via --user option." in result.output
        mock_start.assert_not_called()
        mock_get_ip.assert_not_called()
        mock_subprocess_run.assert_not_called()
        mock_stop.assert_not_called()

def test_connect_command_keep_running(runner, mock_ec2_functions, prepared_config, mock_subprocess_run):
    mock_get_ids, mock_start, mock_stop, mock_get_status = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_get_status.return_value = "running" # Assume it's running initially
    mock_start.return_value = True
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    with patch('ec2ctl.ec2.get_instance_public_ip', return_value="192.168.1.100") as mock_get_ip:
        result = runner.invoke(cli.cli, ['connect', 'dev-server', '--keep-running'])

        assert result.exit_code == 1
        assert "Error: SSH user not specified in config or via --user option." in result.output
        mock_start.assert_not_called()
        mock_get_ip.assert_not_called()
        mock_subprocess_run.assert_not_called()
        mock_stop.assert_not_called() # Should not stop

def test_connect_command_no_ssh_info_in_config(runner, mock_ec2_functions, mock_config_path):
    # Create a config without SSH info for dev-server
    config.create_default_config()
    # Manually modify the config to remove SSH info for dev-server
    cfg = config.get_config()
    cfg['instances']['dev-server'] = 'i-1234567890abcdef0' # Simple ID
    with open(config.CONFIG_PATH, 'w') as f:
        yaml.dump(cfg, f)

    result = runner.invoke(cli.cli, ['connect', 'dev-server'])
    assert result.exit_code == 1
    assert "Error: SSH user not specified in config or via --user option." in result.output

def test_connect_command_override_ssh_info(runner, mock_ec2_functions, prepared_config, mock_subprocess_run):
    mock_get_ids, mock_start, mock_stop, mock_get_status = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_get_status.return_value = "running"
    mock_start.return_value = True
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    with patch('ec2ctl.ec2.get_instance_public_ip', return_value="192.168.1.100") as mock_get_ip:
        result = runner.invoke(cli.cli, ['connect', 'dev-server', '--user', 'testuser', '--key', '~/.ssh/custom_key.pem'])

        assert result.exit_code == 0
        mock_subprocess_run.assert_called_once_with([
            "ssh",
            "-i", os.path.expanduser('~/.ssh/custom_key.pem'),
            "testuser@192.168.1.100"
        ], check=True)

def test_connect_command_no_public_ip(runner, mock_ec2_functions, prepared_config, mock_subprocess_run):
    mock_get_ids, mock_start, mock_stop, mock_get_status = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_get_status.return_value = "running"
    mock_start.return_value = True
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    with patch('ec2ctl.cli._get_instance_details', return_value=("i-1234567890abcdef0", "testuser", "~/.ssh/test_key.pem")) as mock_get_instance_details:
        with patch('ec2ctl.ec2.get_instance_public_ip', return_value=None) as mock_get_ip:
            result = runner.invoke(cli.cli, ['connect', 'dev-server', '--user', 'testuser', '--key', '~/.ssh/test_key.pem'])

        assert result.exit_code == 1
        assert f"Error: Could not get public IP for {mock_get_ids.return_value[0]}. Instance might not have a public IP." in result.output
        mock_stop.assert_not_called() # Should not stop if connection failed
