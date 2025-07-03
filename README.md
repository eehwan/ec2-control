# ec2ctl: Effortless EC2 Instance Control

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg) ![PyPI Version](https://img.shields.io/pypi/v/ec2ctl.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight CLI tool to manage AWS EC2 instances by name or group, designed for developers and DevOps who need a faster, more intuitive way to control their instances without repetitive console access.

## Table of Contents

- [Purpose](#purpose)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [`ec2ctl init`](#ec2ctl-init)
  - [`ec2ctl list`](#ec2ctl-list)
  - [`ec2ctl start`](#ec2ctl-start)
  - [`ec2ctl stop`](#ec2ctl-stop)
  - [`ec2ctl status`](#ec2ctl-status)
- [Error Handling & Troubleshooting](#error-handling--troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Purpose

`ec2ctl` simplifies the management of AWS EC2 instances. It allows you to control instances with intuitive commands based on a local configuration file, eliminating the need for repetitive console access.

## Features

- **Intuitive Commands:** `ec2ctl start dev-server`, `ec2ctl stop all`, `ec2ctl status backend-group`.
- **Flexible Configuration:** Manage instances by name or group using a simple `config.yaml` file.
- **Enhanced User Experience:** Supports `--dry-run`, `--verbose`, and `--yes` options.
- **Robust Error Handling:** Provides clear messages for AWS authentication, instance state, and configuration issues.

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)
- AWS CLI configured with your credentials (`aws configure`)

### Install `ec2ctl`

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/eehwan/ec2-control.git
    cd ec2-control
    ```

2.  **Install in editable mode (for development):**

    ```bash
    pip install -e .
    ```
    This allows changes to the source code to be immediately reflected without reinstallation.

## Configuration

`ec2ctl` uses a YAML configuration file located at `~/.ec2ctl/config.yaml`. You can generate a default configuration file by running:

```bash
ec2ctl init
```

### `config.yaml` Structure

```yaml
default_profile: default
default_region: ap-northeast-2

instances:
  dev-server: i-0abc1234567890
  backend-api:
    - i-01aaa111aaa
    - i-01bbb222bbb
  staging: i-0123staging456
```

-   `default_profile`: (Optional) Your default AWS profile name. Defaults to `default`.
-   `default_region`: (Optional) Your default AWS region. Defaults to `ap-northeast-2`.
-   `instances`: A map of instance names or group names to their corresponding EC2 instance IDs.
    -   Single instance: `dev-server: i-0abc1234567890`
    -   Instance group: `backend-api: [i-01aaa111aaa, i-01bbb222bbb]`

## Usage

All commands support `--profile`, `--region`, `--dry-run`, and `--verbose` options. Commands that modify state also support `--yes` (`-y`).

### `ec2ctl init [--yes]`

Initializes the default `config.yaml` file.

```bash
ec2ctl init
# Overwrite without confirmation
ec2ctl init --yes
```

### `ec2ctl list`

Lists all EC2 instances and groups configured in `~/.ec2ctl/config.yaml`.

```bash
ec2ctl list
```

### `ec2ctl start [name|group]`

Starts the specified EC2 instance(s).

```bash
ec2ctl start dev-server
ec2ctl start backend-api
```

### `ec2ctl stop [name|group]`

Stops the specified EC2 instance(s).

```bash
ec2ctl stop dev-server
ec2ctl stop backend-api
```

### `ec2ctl status [name|group|all]`

Gets the current status of the specified EC2 instance(s).

```bash
ec2ctl status dev-server
ec2ctl status all
```

## Error Handling & Troubleshooting

`ec2ctl` provides informative error messages for common issues:

-   **Config file not found:** Run `ec2ctl init` to create the default configuration.
-   **Instance/Group not found:** Ensure the name is correctly spelled and defined in `config.yaml`.
-   **AWS Authentication/Authorization issues:** Check your AWS CLI configuration (`aws configure`) and IAM policies (e.g., `ec2:StartInstances`, `ec2:StopInstances`, `ec2:DescribeInstances`).
-   **Incorrect Instance State:** Attempting to start an already running instance, or stop an already stopped instance.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
