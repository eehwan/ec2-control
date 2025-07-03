import pytest
from ec2ctl import cli

def test_status_command(runner, mock_ec2_functions, prepared_config):
    mock_get_ids, _, _, mock_status = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    mock_status.return_value = "running"
    
    result = runner.invoke(cli.cli, ['status', 'dev-server'])
    assert result.exit_code == 0
    assert "Instance i-1234567890abcdef0 status: running" in result.output
    mock_status.assert_called_once_with("i-1234567890abcdef0", "default", "ap-northeast-2")
