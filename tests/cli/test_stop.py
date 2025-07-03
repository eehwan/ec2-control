import pytest
from ec2ctl import cli

def test_stop_command(runner, mock_ec2_functions, prepared_config):
    mock_get_ids, _, mock_stop, _ = mock_ec2_functions
    mock_get_ids.return_value = ["i-1234567890abcdef0"]
    
    result = runner.invoke(cli.cli, ['stop', 'dev-server'])
    assert result.exit_code == 0
    assert "Successfully stopped i-1234567890abcdef0." in result.output
    mock_stop.assert_called_once_with("i-1234567890abcdef0", "default", "ap-northeast-2")
