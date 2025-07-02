#!/bin/bash

ENV_FILE=".env"

# ─────────────── 인자 파싱 ───────────────
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --env) ENV_FILE="$2"; shift ;;
    *) echo "[ERROR] 알 수 없는 인자입니다: $1"; exit 1 ;;
  esac
  shift
done

# ─────────────── 디렉토리 기준 경로 설정 ───────────────
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─────────────── .env 파일 로드 및 export ───────────────
if [[ -z "$BASE_DIR/envs/$ENV_FILE" || ! -f "$BASE_DIR/envs/$ENV_FILE" ]]; then
  echo "[ERROR] 유효한 --env 파일 경로를 지정해야 합니다."
  exit 1
fi

set -o allexport
source "$BASE_DIR/envs/$ENV_FILE"
set +o allexport


# ─────────────── 1. EC2 인스턴스 시작 ───────────────
echo "[1/4] EC2 인스턴스($INSTANCE_ID) 시작을 요청합니다..."
aws ec2 start-instances --instance-ids "$INSTANCE_ID" --output text > /dev/null

# ─────────────── 2. 인스턴스가 'running' 상태가 될 때까지 대기 ───────────────
echo "[2/4] 인스턴스가 'running' 상태가 될 때까지 대기 중..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# ─────────────── 3. 퍼블릭 IP 조회 ───────────────
echo "[3/4] 퍼블릭 IP를 조회합니다..."
IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

if [[ -z "$IP" || "$IP" == "None" ]]; then
  echo "[ERROR] 퍼블릭 IP를 조회하는 데 실패했습니다."
  exit 1
fi

# ─────────────── 4. SSH 접속 ───────────────
echo "[4/4] SSH 접속을 시도합니다... ($SSH_USER@$IP)"
sleep 5 # SSH 데몬이 완전히 준비될 때까지 잠시 대기

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "$SSH_KEY_PATH" "$SSH_USER@$IP"

echo "[SUCCESS] SSH 연결이 종료되었습니다."