import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_ec2_functions():
    with patch('ec2ctl.ec2.get_instance_ids_from_names') as mock_get_ids:
        with patch('ec2ctl.ec2.start_instance') as mock_start:
            with patch('ec2ctl.ec2.stop_instance') as mock_stop:
                with patch('ec2ctl.ec2.get_instance_status') as mock_status:
                    yield mock_get_ids, mock_start, mock_stop, mock_status
