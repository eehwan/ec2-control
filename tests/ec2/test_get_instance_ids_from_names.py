import pytest
from ec2ctl import ec2
from ec2ctl.exceptions import ConfigError

def test_get_instance_ids_from_names():
    config_data = {
        "instances": {
            "dev-server": "i-1234567890abcdef0",
            "backend-api": [
                "i-abcdef12345678901",
                "i-abcdef12345678902",
            ],
            "staging": "i-fedcba98765432100",
        }
    }
    assert ec2.get_instance_ids_from_names(["dev-server"], config_data) == ["i-1234567890abcdef0"]
    assert sorted(ec2.get_instance_ids_from_names(["backend-api"], config_data)) == sorted([
        "i-abcdef12345678901",
        "i-abcdef12345678902",
    ])
    assert sorted(ec2.get_instance_ids_from_names(["dev-server", "backend-api"], config_data)) == sorted([
        "i-1234567890abcdef0",
        "i-abcdef12345678901",
        "i-abcdef12345678902",
    ])
    with pytest.raises(ConfigError, match="not found in config"):
        ec2.get_instance_ids_from_names(["non-existent"], config_data)
