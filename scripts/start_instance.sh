#!/bin/bash

echo "[EC2] 인스턴스를 시작합니다..."

aws ec2 start-instances \
  --instance-ids "$INSTANCE_ID" \
  --output text > /dev/null

echo "[EC2] 인스턴스 시작 요청 완료"