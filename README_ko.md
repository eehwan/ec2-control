# ec2ctl: 간편한 EC2 인스턴스 제어

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg) ![PyPI Version](https://img.shields.io/pypi/v/ec2ctl.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

Read this in other languages: [한국어](https://github.com/eehwan/ec2-control/blob/main/README_ko.md) | [English](https://github.com/eehwan/ec2-control/blob/main/README.md)

---

EC2 인스턴스를 켜고 끌 때마다 AWS 콘솔에 접속해서 IP를 복사하고, 연결 정보를 일일이 입력하기 귀찮으셨나요?

**`ec2ctl`은 개발용 EC2 인스턴스를 자주 켜고 끄는 개발자를 위해 만들어진 가볍고 직관적인 CLI 도구입니다.**  
더 빠르게, 더 간편하게 인스턴스를 제어하고 SSH로 연결할 수 있도록 도와줍니다. 콘솔에 들어가지 않고도 원하는 작업을 터미널에서 한 줄로 처리해보세요.

---

## 목차

- [사용 목적](#사용-목적)
- [주요 기능](#주요-기능)
- [설치 방법](#설치-방법)
- [설정 방법](#설정-방법)
- [사용법](#사용법)
- [문제 해결](#문제-해결)
- [Contributing](#contributing)
- [License](#license)

---

## 사용 목적

많은 개발자들이 AWS 비용을 아끼기 위해 EC2 인스턴스를 필요할 때만 켜서 개발 서버로 사용합니다.  
하지만 콘솔을 켜고 인스턴스를 찾아서 시작하고, 그때마다 바뀌는 IP로 SSH 연결을 하는 건 꽤 번거로운 일이죠.

`ec2ctl`은 이런 귀찮은 반복을 없애기 위해 만들어졌습니다.

- 간단한 명령어 하나로 EC2 인스턴스를 켜거나 끌 수 있고
- IP가 바뀌어도 자동으로 연결되며
- 자주 쓰는 인스턴스를 설정 파일로 이름 붙여 관리할 수 있습니다
- 더 이상 AWS 콘솔에 들어갈 필요도 없습니다

---

## 주요 기능

- **직관적인 명령어**: `ec2ctl start dev-server`, `ec2ctl stop all` 등으로 바로 실행
- **유연한 설정**: 인스턴스를 이름 또는 그룹 단위로 구성하여 관리
- **사용자 친화적인 옵션**: `--dry-run`, `--verbose`, `--yes` 등 지원
- **에러 처리 강화**: AWS 인증, 설정 문제, 인스턴스 상태에 대한 명확한 안내 제공
- **SSH 연결 지원**: SSH로 바로 접속 가능, 연결 종료 시 자동 종료 옵션 제공

---

## 설치 방법

### 사전 준비

- Python 3.7 이상
- pip (Python 패키지 관리자)
- AWS CLI 설치 및 인증 완료 (`aws configure` 실행)

### PyPI에서 설치

```bash
pip install ec2ctl
````

### 개발용 설치 (수정 및 기여 시)

```bash
git clone https://github.com/eehwan/ec2-control.git
cd ec2-control
pip install -e .
```

---

## 설정 방법

`ec2ctl`은 `~/.ec2ctl/config.yaml` 파일을 설정 파일로 사용합니다.
`ec2ctl init` 명령어는 이제 AWS 프로필과 리전을 선택하도록 대화형으로 안내하며, 사용자의 EC2 인스턴스를 자동으로 탐색하여 이를 기반으로 `config.yaml`을 생성합니다.

```bash
ec2ctl init
```

### 생성된 `config.yaml` 구조

`ec2ctl init` 명령어는 사용자의 EC2 인스턴스를 탐색하여 이를 기반으로 `config.yaml`을 생성합니다. 다음과 유사하게 보일 것입니다:

```yaml
default_profile: 선택된-프로필
default_region: 선택된-리전

instances:
  web-1:
    id: i-0123456789abcdef0
    ssh_user: ec2-user # 자동 추정됨, 필요시 확인 및 변경
    ssh_key_path: ~/.ssh/web-1-key.pem # 자동 추정됨, 필요시 확인 및 변경
  web-2:
    id: i-fedcba9876543210
    ssh_user: ubuntu # 자동 추정됨, 필요시 확인 및 변경
    ssh_key_path: ~/.ssh/web-2-key.pem # 자동 추정됨, 필요시 확인 및 변경
  # ... 그 외 탐색된 인스턴스
```

-   `default_profile`: `init` 과정에서 선택된 기본 AWS 프로필 이름.
-   `default_region`: `init` 과정에서 선택된 기본 AWS 리전.
-   `instances`: 탐색된 EC2 인스턴스 이름(또는 Name 태그가 없는 경우 ID)과 해당 세부 정보의 맵.
    -   `id`: EC2 인스턴스 ID.
    -   `ssh_user`: 자동 추정된 SSH 사용자(기본값은 `ec2-user`). **인스턴스의 AMI에 따라 이를 확인하고 변경해야 합니다(예: Ubuntu AMI의 경우 `ubuntu`).**
    -   `ssh_key_path`: 인스턴스에 연결된 키 페어 이름을 기반으로 자동 추정된 SSH 개인 키 경로. **이 경로를 확인하고 실제 개인 키 파일을 가리키는지 확인해야 합니다.** 키 이름이 발견되지 않으면 플레이스홀더가 사용됩니다.

**인스턴스 또는 그룹 수동 추가:**

`ec2ctl init`이 초기 설정을 생성한 후, `~/.ec2ctl/config.yaml` 파일을 수동으로 편집하여 더 많은 인스턴스를 추가하거나 그룹을 정의할 수 있습니다. 인스턴스 그룹 또는 간단한 ID 항목을 정의하는 방법에 대한 예시는 `config.example.yaml`을 참조하십시오.

```yaml
# config.example.yaml에서 수동으로 추가할 수 있는 항목 예시:
instances:
  # ... (기존에 탐색된 인스턴스)

  dev-server:
    id: i-0abc1234567890
    ssh_user: ec2-user
    ssh_key_path: ~/.ssh/my-key.pem
    ssh_port: 2222
  backend-api:
    - id: i-01aaa111aaa
      ssh_user: ubuntu
      ssh_key_path: ~/.ssh/backend_key.pem
    - id: i-01bbb222bbb
      ssh_user: ubuntu
      ssh_key_path: ~/.ssh/backend_key.pem
  staging: i-0123staging456
```

-   `default_profile`: `init` 과정에서 선택된 기본 AWS 프로필 이름.
-   `default_region`: `init` 과정에서 선택된 기본 AWS 리전.
-   `instances`: 탐색된 EC2 인스턴스 이름(또는 Name 태그가 없는 경우 ID)과 해당 세부 정보의 맵. 여기에 수동으로 항목을 추가할 수도 있습니다.
    -   `id`: EC2 인스턴스 ID.
    -   `ssh_user`: 자동 추정된 SSH 사용자(기본값은 `ec2-user`). **인스턴스의 AMI에 따라 이를 확인하고 변경해야 합니다(예: Ubuntu AMI의 경우 `ubuntu`).**
    -   `ssh_key_path`: 인스턴스에 연결된 키 페어 이름을 기반으로 자동 추정된 SSH 개인 키 경로. **이 경로를 확인하고 실제 개인 키 파일을 가리키는지 확인해야 합니다.** 키 이름이 발견되지 않으면 플레이스홀더가 사용됩니다.

여전히 이 파일을 수동으로 편집하여 인스턴스 그룹을 추가하거나 세부 정보를 수정할 수 있습니다.

---

## 사용법

모든 명령어는 `--profile`, `--region`, `--dry-run`, `--verbose` 옵션을 지원합니다.
상태를 변경하는 명령어는 `--yes` (`-y`)도 지원합니다.

### 인스턴스 설정 초기화

AWS 계정에서 EC2 인스턴스를 탐색하여 설정 파일을 초기화합니다. AWS 프로필과 리전을 선택하라는 메시지가 표시됩니다.

```bash
ec2ctl init
ec2ctl init --yes  # 기존 파일 덮어쓰기
```

### 인스턴스 목록 확인

```bash
ec2ctl list
```

### 인스턴스 시작

```bash
ec2ctl start dev-server
ec2ctl start backend-api
```

### 인스턴스 중지

```bash
ec2ctl stop dev-server
ec2ctl stop backend-api
```

### 인스턴스 상태 확인

```bash
ec2ctl status dev-server
ec2ctl status all
```

### SSH 연결

필요할 경우 인스턴스를 자동으로 시작한 뒤, SSH로 접속합니다.
기본적으로 SSH 연결을 끊으면 인스턴스는 자동으로 중지됩니다. (`--keep-running` 옵션으로 유지 가능)

```bash
# 기본 SSH 연결 (연결 종료 시 자동 중지)
ec2ctl connect dev-server

# 포트, 사용자, 키 파일 직접 지정
ec2ctl connect dev-server --port 2222
ec2ctl connect dev-server --user admin --key ~/.ssh/custom.pem

# 연결 종료 후에도 인스턴스를 계속 실행
ec2ctl connect dev-server --keep-running
```

---

## 문제 해결

* **Config file not found**: `ec2ctl init`으로 새 설정 파일을 생성하세요.
* **Instance/Group not found**: `config.yaml`에 정의된 이름이 맞는지 확인하세요.
* **AWS Authentication/Authorization issues**: `aws configure`를 통해 자격 증명 및 권한을 확인하세요.
* **Incorrect Instance State**: 이미 실행 중인 인스턴스를 시작하려고 시도하거나, 이미 중지된 인스턴스를 중지하려고 시도하는 경우입니다.
* **SSH Connection Issues**: 퍼블릭 IP 확인, 보안 그룹에 포트 22 허용 여부, SSH 키 경로 및 권한을 확인하세요.

---

## Contributing

버그 제보, 개선 제안, PR 모두 환영합니다!
작은 기여도 큰 도움이 됩니다 :)

---

## License

이 프로젝트는 MIT License를 따릅니다.
자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.