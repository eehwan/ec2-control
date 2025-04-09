#!/bin/bash

# .env 파일 불러오기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

set -e  # 에러 발생 시 즉시 종료 (안정성 높음)

echo "[EC2] 인스턴스 시작 중..."
START_OUTPUT=$(aws ec2 start-instances --instance-ids "$INSTANCE_ID" 2>&1) || {
  echo "[ERROR] 인스턴스 시작 실패:"
  echo "$START_OUTPUT"
  exit 1
}

echo "[EC2] 퍼블릭 IP 할당 대기 중..."
sleep 10

IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "[EC2] 인스턴스가 시작되었고 IP는: $IP"

