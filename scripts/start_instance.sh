#!/bin/bash

echo "[EC2] 인스턴스($INSTANCE_ID) 시작을 요청합니다..."

aws ec2 start-instances \
  --instance-ids "$INSTANCE_ID" \
  --output text > /dev/null

echo "[EC2] 인스턴스가 'running' 상태가 될 때까지 대기 중..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

echo "[EC2] 인스턴스 시작 및 준비 완료"