import pytest
import yaml
from ec2ctl import config
from ec2ctl.exceptions import ConfigError

def test_get_config_file_not_found(mock_config_path):
    with pytest.raises(ConfigError, match="Config file not found"):
        config.get_config()

def test_get_config_invalid_yaml(mock_config_path):
    with open(config.CONFIG_PATH, 'w') as f:
        f.write("invalid: - yaml")
        
    with pytest.raises(ConfigError, match="Error parsing config file"):
        config.get_config()
