import os
import pytest
from ec2ctl import cli
from ec2ctl import config

def test_init_command(runner, mock_config_path):
    result = runner.invoke(cli.cli, ['init'])
    assert result.exit_code == 0
    assert "Created default config file" in result.output
    assert os.path.exists(config.CONFIG_PATH)

def test_init_command_overwrite_no(runner, prepared_config):
    result = runner.invoke(cli.cli, ['init'], input='n\n')
    assert result.exit_code == 0
    assert "Aborted." in result.output

def test_init_command_overwrite_yes(runner, prepared_config):
    result = runner.invoke(cli.cli, ['init', '--yes'])
    assert result.exit_code == 0
    assert "Created default config file" in result.output

