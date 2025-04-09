# EC2 & DuckDNS Control Scripts

AWS EC2 인스턴스를 시작하고 일정 시간 후 자동으로 종료하며,  
현재 퍼블릭 IP를 DuckDNS에 자동 등록하는 셸 스크립트 기반 자동화 도구입니다.

---

## 디렉토리 구조

```
ec2-duckdns-control/
├── envs/
│   ├── dev.env
│   ├── prod.env
│   └── .env.example      ← 템플릿만 깃에 포함
├── scripts/
│   ├── start_instance.sh
│   ├── stop_instance.sh
│   ├── update_dns.sh
│   └── wait_and_shutdown.sh
├── start_and_shutdown.sh
├── shutdown.log          ← nohup 로그
├── README.md
└── .gitignore
```

## 주요 스크립트 설명

| 파일명 | 역할 |
|--------|------|
| `start_and_shutdown.sh` | `.env`를 로드하고 전체 자동화 흐름을 실행 (시작 → DNS 등록 → 자동 종료 예약) |
| `scripts/start_instance.sh` | EC2 인스턴스를 시작하고 시작 요청 완료 메시지를 출력 |
| `scripts/update_dns.sh` | EC2 인스턴스의 퍼블릭 IP를 DuckDNS에 매핑 |
| `scripts/wait_and_shutdown.sh` | 설정된 시간 후 EC2 인스턴스를 자동 종료 |
| `scripts/stop_instance.sh` | EC2 인스턴스를 수동으로 즉시 종료 |

---

## ⚙️ 사용 방법

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


> 💡 이 스크립트를 사용하려면 DuckDNS 계정을 생성하고, 서브도메인과 토큰을 발급받아야 합니다.

### 2. DuckDNS 계정 생성 및 .env 설정

1. https://www.duckdns.org에 접속하여 GitHub/Google 등으로 로그인

2. 원하는 서브도메인 등록 (예: myproject.duckdns.org)

3. 상단에 표시되는 토큰 복사

#### .env 파일 예시 (envs/dev.env):

```env
INSTANCE_ID=i-xxxxxxxxxxxxxxxxx     # EC2 인스턴스 ID
DUCKDNS_DOMAIN=your-subdomain       # DuckDNS 서브도메인 (예: myproject)
DUCKDNS_TOKEN=your-duckdns-token    # DuckDNS API 토큰
```

### 3. 실행 권한 부여

```bash
chmod +x start_and_shutdown.sh
chmod +x scripts/*.sh
```

### 4. 스크립트 실행 예시

```bash
# 1시간 후 종료 (기본값)
./start_and_shutdown.sh --env dev.env

# 30분 후 종료
./start_and_shutdown.sh --env dev.env --wait 1800
```

### 5. 수동으로 종료하고 싶을 경우

```bash
source envs/dev.env
./scripts/stop_instance.sh
```