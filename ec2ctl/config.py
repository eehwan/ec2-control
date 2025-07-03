import os
import yaml
from .exceptions import ConfigError

CONFIG_DIR = os.path.expanduser("~/.ec2ctl")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

def get_config():
    """Loads the config file."""
    if not os.path.exists(CONFIG_PATH):
        raise ConfigError(f"Config file not found: {CONFIG_PATH}. Please run 'ec2ctl init' to create one.")
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing config file {CONFIG_PATH}: {e}")

def create_default_config():
    """Creates the default config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    default_config = {
        'default_profile': 'default',
        'default_region': 'ap-northeast-2',
        'instances': {
            'dev-server': 'i-0abc1234567890',
            'backend-api': [
                'i-01aaa111aaa',
                'i-01bbb222bbb',
            ],
            'staging': 'i-0123staging456',
        }
    }
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
