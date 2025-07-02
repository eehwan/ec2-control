# EC2 Instance Control Scripts

AWS EC2 인스턴스를 시작하고 종료하며, SSH 접속을 자동화하는 셸 스크립트 기반 도구입니다.

---

## 디렉토리 구조

```
ec2-instance-control/
├── envs/
│   ├── dev.env
│   ├── prod.env
│   └── .env.example      ← 템플릿만 깃에 포함
├── scripts/
│   ├── start_instance.sh
│   ├── stop_instance.sh
│   └── wait_and_shutdown.sh
├── open.sh
├── close.sh
├── connect.sh
├── install.sh            ← 새로운 설치 스크립트
├── shutdown.log          ← nohup 로그
├── README.md
└── .gitignore
```

## 주요 스크립트 설명

| 파일명 | 역할 |
|--------|------|
| `install.sh` | `ec2ctl` 셸 함수를 설치하여 스크립트 실행을 간소화 |
| `open.sh` | `.env`를 로드하고 전체 자동화 흐름을 실행 (시작 → 자동 종료 예약) |
| `close.sh` | `.env`를 로드하고 인스턴스 종료 |
| `connect.sh` | `.env`를 로드하고 EC2 인스턴스를 시작한 후 SSH로 접속 |
| `scripts/start_instance.sh` | EC2 인스턴스를 시작하고 시작 요청 완료 메시지를 출력 |
| `scripts/wait_and_shutdown.sh` | 설정된 시간 후 EC2 인스턴스를 자동 종료 |
| `scripts/stop_instance.sh` | EC2 인스턴스를 수동으로 즉시 종료 |

---

## ⚙️ 필수 설정

### 1. AWS CLI 설치 및 설정

> 💡 AWS CLI가 반드시 설치되어 있어야 하며, 적절한 자격 증명이 필요합니다.

#### AWS CLI 설치 (Ubuntu 기준) :

```bash
sudo apt update && sudo apt install -y awscli
```

```bash
aws configure
```

입력 항목:

- AWS Access Key ID: IAM 사용자용 키

- AWS Secret Access Key: 위 키의 비밀 키

- Default region name: 예: ap-northeast-2 (서울 리전)

- Default output format: json 또는 text

> ⚠️ 해당 키는 EC2 인스턴스에 대해 start, stop, describe-instances 권한을 반드시 가져야 합니다.
권한이 부족하면 스크립트가 실패합니다.

### 2. .env 파일 설정

`.env` 파일에는 EC2 인스턴스 ID, SSH 키 경로, SSH 사용자 이름이 포함되어야 합니다. `envs/` 디렉토리에 `dev.env`, `prod.env` 등 환경별 파일을 생성하여 관리할 수 있습니다.

```env
INSTANCE_ID=i-xxxxxxxxxxxxxxxxx     # EC2 인스턴스 ID
SSH_KEY_PATH="/path/to/your-key.pem"  # SSH 키 파일의 절대 경로
SSH_USER=ubuntu                         # EC2 인스턴스 사용자 이름 (예: ubuntu, ec2-user)
```

---

## 🚀 빠른 시작

`install.sh` 스크립트를 실행하여 `ec2ctl` 셸 함수를 설치하세요. 이 함수를 통해 EC2 제어 스크립트를 더 쉽게 실행할 수 있습니다.

```bash
git clone https://github.com/eehwan/ec2-instance-control
cd ec2-instance-control
chmod +x install.sh # 실행 권한 부여
./install.sh        # 설치 스크립트 실행
```

**주의:** `install.sh` 스크립트는 `.zshrc` 또는 `.bashrc`와 같은 셸 설정 파일을 수정합니다. 스크립트 실행 전에 내용을 확인하시고, 실행 중 동의 여부를 묻는 프롬프트에 'y'를 입력해야 합니다.

### 스크립트 실행 예시 (`ec2ctl` 함수 사용)

`install.sh`를 통해 `ec2ctl` 함수를 설치한 후, 터미널에서 다음 명령어를 사용하여 스크립트를 실행할 수 있습니다.

```bash
# 기본 .env 파일을 사용하여 EC2 인스턴스 시작 및 2시간 후 자동 종료 예약
ec2ctl open

# 'dev.env' 파일을 사용하여 EC2 인스턴스 시작 및 30분(1800초) 후 자동 종료 예약
ec2ctl open dev --wait 1800

# 'dev.env' 파일을 사용하여 EC2 인스턴스 즉시 종료
ec2ctl close dev

# 'prod.env' 파일을 사용하여 EC2 인스턴스 시작 후 SSH 접속
ec2ctl connect prod
```

**`ec2ctl` 함수 사용법:**

```bash
ec2ctl <스크립트_이름> [환경_이름] [스크립트_추가_인자...]
```

*   `<스크립트_이름>`: `open`, `close`, `connect` 중 하나.
*   `[환경_이름]`: 사용할 `.env` 파일의 이름 (예: `dev`, `prod`). 지정하지 않으면 `envs/.env` 파일을 사용합니다.
*   `[스크립트_추가_인자...]`: `open.sh`의 `--wait`와 같이 각 스크립트가 받는 추가 인자들.

---

## 🗑️ 정리 (인스턴스 종료)

EC2 인스턴스를 수동으로 즉시 종료하려면 `ec2ctl close` 명령을 사용하세요.

```bash
ec2ctl close dev
```