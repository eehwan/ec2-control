import os
import pytest
from ec2ctl import config

def test_create_default_config(mock_config_path):
    config.create_default_config()
    assert os.path.exists(config.CONFIG_PATH)
    
    loaded_config = config.get_config()
    assert loaded_config['default_profile'] == 'default'
    assert loaded_config['default_region'] == 'ap-northeast-2'
    assert 'dev-server' in loaded_config['instances']
