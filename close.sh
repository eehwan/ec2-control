#!/bin/bash

WAIT_SECONDS=7200
ENV_FILE=".env"

# ─────────────── 인자 파싱 ───────────────
while [[ "$#" -gt 0 ]]; do
  case $1 in
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

# ─────────────── EC2 종료 ───────────────
echo "[EC2] 인스턴스 종료 요청 중..."
"$BASE_DIR/scripts/stop_instance.sh"
echo "[EC2] 종료 요청 완료."