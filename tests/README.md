# Tests for ec2ctl

This directory contains all unit and integration tests for the `ec2ctl` CLI tool.

## Test Structure

The tests are organized into subdirectories mirroring the main application's module structure (`cli`, `ec2`, `config`). This modular approach enhances readability, maintainability, and test isolation.

```
tests/
├── conftest.py             # Global fixtures accessible by all tests
├── cli/                    # Tests for the CLI commands (ec2ctl/cli.py)
│   ├── __init__.py
│   ├── conftest.py         # CLI-specific fixtures (e.g., mock_ec2_functions)
│   ├── test_init.py
│   ├── test_list.py
│   ├── test_start.py
│   ├── test_stop.py
│   ├── test_status.py
│   └── test_connect.py
├── ec2/                    # Tests for AWS EC2 interactions (ec2ctl/ec2.py)
│   ├── __init__.py
│   ├── conftest.py         # EC2-specific fixtures (e.g., mocked AWS credentials, EC2 client, instances)
│   ├── test_get_instance_ids_from_names.py
│   ├── test_get_instance_status.py
│   ├── test_start_instance.py
│   └── test_stop_instance.py
└── config/                 # Tests for configuration handling (ec2ctl/config.py)
    ├── __init__.py
    ├── test_create_default_config.py
    └── test_get_config.py
```

## Running Tests

To run all tests, navigate to the project root directory and execute:

```bash
python3 -m pytest tests/
```

### Running Specific Tests

-   **Run tests in a specific directory:**

    ```bash
    python3 -m pytest tests/cli/
    ```

-   **Run tests in a specific file:**

    ```bash
    python3 -m pytest tests/cli/test_start.py
    ```

-   **Run a specific test function:**

    ```bash
    python3 -m pytest tests/cli/test_start.py::test_start_command_dry_run
    ```

## Fixtures

Fixtures are used to set up a baseline for tests and ensure a clean state for each test run. They are defined in `conftest.py` files at different levels:

-   **`tests/conftest.py`:** Contains global fixtures used across multiple test modules (e.g., `runner`, `mock_config_path`, `prepared_config`).
-   **`tests/cli/conftest.py`:** Contains fixtures specific to CLI command tests (e.g., `mock_ec2_functions`).
-   **`tests/ec2/conftest.py`:** Contains fixtures specific to EC2 interaction tests (e.g., `aws_credentials`, `ec2_client`, `running_instance`, `stopped_instance`).

## Mocking

`unittest.mock` and `moto` libraries are used extensively to mock external dependencies, especially AWS API calls. This ensures tests are fast, reliable, and do not incur actual AWS costs or modify real resources.

## Test Coverage

(Optional: You can add information about test coverage here, e.g., how to run coverage reports and what the target coverage is.)
