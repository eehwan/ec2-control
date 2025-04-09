#!/bin/bash

echo "[EC2] 인스턴스 종료 중..."
aws ec2 stop-instances \
    --instance-ids "$INSTANCE_ID" \
    --output text > /dev/null