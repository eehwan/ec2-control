import os
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from ec2ctl import config

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_config_path(tmp_path):
    original_config_dir = config.CONFIG_DIR
    original_config_path = config.CONFIG_PATH
    
    config.CONFIG_DIR = str(tmp_path / ".ec2ctl")
    config.CONFIG_PATH = str(tmp_path / ".ec2ctl" / "config.yaml")
    
    os.makedirs(config.CONFIG_DIR, exist_ok=True)
    
    yield
    
    config.CONFIG_DIR = original_config_dir
    config.CONFIG_PATH = original_config_path

@pytest.fixture
def prepared_config(mock_config_path):
    config.create_default_config()
    yield
