#!/bin/bash

LOCKFILE="/tmp/ec2_shutdown_lock_${INSTANCE_ID}.pid"
WAIT_SECONDS=${1:-7200}  # 기본 2시간

if [ -f "$LOCKFILE" ]; then
  OLD_PID=$(cat "$LOCKFILE")
  if ps -p "$OLD_PID" > /dev/null 2>&1; then
    echo "[WARNING] 이미 종료 예약이 진행 중입니다. (PID: $OLD_PID)"
    exit 1
  else
    rm -f "$LOCKFILE"
  fi
fi

echo $$ > "$LOCKFILE"

echo "[TIMER] $((WAIT_SECONDS / 60))분 후 EC2 인스턴스를 종료합니다..."
sleep "$WAIT_SECONDS"

"$BASE_DIR/scripts/stop_instance.sh"
rm -f "$LOCKFILE"
