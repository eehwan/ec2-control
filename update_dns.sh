#!/bin/bash

# .env 파일 불러오기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

set -e  # 에러 발생 시 즉시 종료 (안정성 높음)

echo "[DNS] EC2 IP 조회 중..."
IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text) || {
  echo "$IP"
  exit 1
}

echo "[DNS] 현재 퍼블릭 IP는: $IP"
echo "[DNS] DuckDNS에 매핑 중..."

curl -s "https://www.duckdns.org/update?domains=$DUCKDNS_DOMAIN&token=$DUCKDNS_TOKEN&ip=$IP"

echo "[DNS] DuckDNS 업데이트 완료: $DUCKDNS_DOMAIN → $IP"

