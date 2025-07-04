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
  - [`ec2ctl connect`](#ec2ctl-connect)
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
- **SSH Connection:** Connect directly to instances, with optional automatic stopping on disconnect.

## Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)
- AWS CLI configured with your credentials (`aws configure`)

### Install `ec2ctl`

You can install `ec2ctl` directly from PyPI using pip:

```bash
pip install ec2ctl
```

#### For Development

If you plan to contribute or modify the source code, you can install it in editable mode:

```bash
git clone https://github.com/eehwan/ec2-control.git
cd ec2-control
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
  dev-server:
    id: i-0abc1234567890
    ssh_user: ec2-user
    ssh_key_path: ~/.ssh/id_rsa
    ssh_port: 2222 # Optional SSH port
  backend-api:
    - id: i-01aaa111aaa
      ssh_user: ubuntu
      ssh_key_path: ~/.ssh/backend_key.pem
    - id: i-01bbb222bbb
      ssh_user: ubuntu
      ssh_key_path: ~/.ssh/backend_key.pem
  staging: i-0123staging456 # Simple ID definition still supported
```

-   `default_profile`: (Optional) Your default AWS profile name. Defaults to `default`.
-   `default_region`: (Optional) Your default AWS region. Defaults to `ap-northeast-2`.
-   `instances`: A map of instance names or group names to their corresponding EC2 instance IDs and optional SSH details.
    -   Single instance with SSH details: `dev-server: { id: ..., ssh_user: ..., ssh_key_path: ..., ssh_port: ... }`
    -   Instance group with SSH details: `backend-api: [ { id: ..., ssh_user: ..., ssh_key_path: ... }, ... ]`
    -   Simple ID definition is still supported: `staging: i-0123staging456`

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

### `ec2ctl connect [name] [--user USER] [--key KEY_PATH] [--port PORT] [--keep-running]`

Connects to an EC2 instance via SSH, starting it if necessary. By default, the instance will be stopped when the SSH session disconnects.

-   `name`: The name of the instance or group as defined in `config.yaml`.
-   `--user USER`: Override the SSH user defined in config.
-   `--key KEY_PATH`: Override the path to the SSH private key file defined in config.
-   `--port PORT`: Override the SSH port defined in config.
-   `--keep-running`: Keep the instance running after the SSH session disconnects.

```bash
# Connect to dev-server, stop on disconnect (default)
ec2ctl connect dev-server

# Connect to dev-server with a specific port
ec2ctl connect dev-server --port 2222

# Connect to dev-server, keep running on disconnect
ec2ctl connect dev-server --keep-running

# Connect with overridden user and key
ec2ctl connect dev-server --user admin --key ~/.ssh/my_custom_key.pem
```

## Error Handling & Troubleshooting

`ec2ctl` provides informative error messages for common issues:

-   **Config file not found:** Run `ec2ctl init` to create the default configuration.
-   **Instance/Group not found:** Ensure the name is correctly spelled and defined in `config.yaml`.
-   **AWS Authentication/Authorization issues:** Check your AWS CLI configuration (`aws configure`) and IAM policies (e.g., `ec2:StartInstances`, `ec2:StopInstances`, `ec2:DescribeInstances`).
-   **Incorrect Instance State:** Attempting to start an already running instance, or stop an already stopped instance.
-   **SSH Connection Issues:** Ensure the instance has a public IP, security groups allow SSH (port 22), and the SSH key path/permissions are correct.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.