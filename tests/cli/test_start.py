import pytest
from ec2ctl import cli
from ec2ctl.exceptions import AwsError

def test_start_command(runner, mock_ec2_functions, prepared_config):
    mock_get_ids, mock_start, _, _ = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    
    result = runner.invoke(cli.cli, ['start', 'dev-server'])
    assert result.exit_code == 0
    assert "Successfully started i-1234567890abcdef0." in result.output
    mock_start.assert_called_once_with("i-1234567890abcdef0", "default", "ap-northeast-2")

def test_start_command_dry_run(runner, mock_ec2_functions, prepared_config):
    mock_get_ids, mock_start, _, _ = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    
    result = runner.invoke(cli.cli, ['start', 'dev-server', '--dry-run'])
    assert result.exit_code == 0
    assert "Dry run: Would start i-1234567890abcdef0" in result.output
    mock_start.assert_not_called()

def test_start_command_aws_error(runner, mock_ec2_functions, prepared_config):
    mock_get_ids, mock_start, _, _ = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_start.side_effect = AwsError("Permission denied")
    
    result = runner.invoke(cli.cli, ['start', 'dev-server'])
    assert isinstance(result.exception, SystemExit)
    assert result.exception.code == 1
    assert "Error: Permission denied" in result.output
