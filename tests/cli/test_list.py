import pytest
from ec2ctl import cli

def test_list_command(runner, prepared_config):
    result = runner.invoke(cli.cli, ['list'])
    assert result.exit_code == 0
    assert "dev-server" in result.output
    assert "backend-api" in result.output

def test_list_command_no_config(runner, mock_config_path):
    result = runner.invoke(cli.cli, ['list'])
    assert isinstance(result.exception, SystemExit)
    assert result.exception.code == 1
    assert "Config file not found" in result.output
