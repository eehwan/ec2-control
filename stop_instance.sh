#!/bin/bash

# .env 파일 불러오기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

echo "[EC2] 인스턴스 종료 중..."
aws ec2 stop-instances --instance-ids $INSTANCE_ID > /dev/null

echo "[EC2] 종료 요청 완료. 몇 초 후 종료됩니다."

