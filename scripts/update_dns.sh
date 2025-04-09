#!/bin/bash

IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text 2>/dev/null)

if [[ -z "$IP" || "$IP" == "None" ]]; then
  echo "[ERROR] 퍼블릭 IP 조회 실패"
  exit 1
fi

echo "[DNS] DuckDNS 업데이트 중... ($DUCKDNS_DOMAIN → $IP)"
curl -s "https://www.duckdns.org/update?domains=$DUCKDNS_DOMAIN&token=$DUCKDNS_TOKEN&ip=$IP" > /dev/null
echo "[DNS] 완료: $IP"
