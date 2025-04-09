#!/bin/bash

WAIT_SECONDS=7200
ENV_FILE=".env"

# ─────────────── 인자 파싱 ───────────────
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --wait) WAIT_SECONDS="$2"; shift ;;
    --env) ENV_FILE="$2"; shift ;;
    *) echo "[ERROR] Unknown parameter: $1"; exit 1 ;;
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

# ─────────────── EC2 인스턴스 시작 ───────────────
"$BASE_DIR/scripts/start_instance.sh"

# ─────────────── 퍼블릭 IP 할당 대기 (10초) ───────────────
echo "[INFO] 퍼블릭 IP 할당 대기 중 (10초)..."
sleep 10

# ─────────────── DuckDNS에 퍼블릭 IP 등록 ───────────────
"$BASE_DIR/scripts/update_dns.sh"

# ─────────────── 종료 타이머 실행 (백그라운드) ───────────────
nohup "$BASE_DIR/scripts/wait_and_shutdown.sh" "$WAIT_SECONDS" > shutdown.log 2>&1 &

echo "[INFO] 종료 예약이 백그라운드로 등록되었습니다. $((WAIT_SECONDS / 60))분 후 인스턴스 종료 예정."