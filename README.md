# EC2 & DuckDNS Control Scripts

간단한 셸 스크립트를 이용해 AWS EC2 인스턴스를 시작/종료하고,  
현재 퍼블릭 IP를 DuckDNS에 자동으로 매핑하는 자동화 도구입니다.

---

## 🧩 구성 스크립트

| 파일명 | 설명 |
|--------|------|
| `start_instance.sh` | EC2 인스턴스를 시작하고 퍼블릭 IP를 출력합니다 |
| `stop_instance.sh` | EC2 인스턴스를 종료합니다 |
| `update_dns.sh` | 현재 EC2 인스턴스의 퍼블릭 IP를 DuckDNS에 등록합니다 |

---

## ⚙️ 사용 방법

### 1. 환경설정 AWS CLI 설치 및 설정

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

### 2. `.env` 파일 생성

> 💡 이 스크립트를 사용하려면 DuckDNS 계정을 생성하고, 서브도메인과 토큰을 발급받아야 합니다.

스크립트와 같은 디렉토리에 `.env` 파일을 생성하고 아래와 같이 작성하세요:

```env
INSTANCE_ID=i-xxxxxxxxxxxxxxxxx     # EC2 인스턴스 ID
DUCKDNS_DOMAIN=your-subdomain       # DuckDNS 서브도메인 (예: myproject)
DUCKDNS_TOKEN=your-duckdns-token    # DuckDNS API 토큰
```

### 3. 실행 권한 부여

```bash
chmod +x *.sh
```

### 4. 스크립트 실행 예시

```bash
./start_instance.sh
./update_dns.sh
./stop_instance.sh
```