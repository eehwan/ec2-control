#!/bin/bash

# 이 스크립트가 위치한 디렉토리를 프로젝트 루트로 설정합니다.
# 사용자가 프로젝트를 어디에 클론하든 상관없이 올바른 경로를 찾습니다.
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ec2ctl 함수 정의
# PROJECT_DIR 변수는 이 install.sh 스크립트가 실행될 때의 실제 경로로 대체됩니다.
# heredoc의 EOF를 따옴표로 묶어 내부 변수 확장을 방지하고, PROJECT_DIR만 별도로 삽입합니다.
EC2CTL_FUNCTION=$(cat <<'EOF'
# --- EC2 Control Scripts Function ---
# EC2 인스턴스 제어 스크립트를 쉽게 실행하기 위한 함수
# 사용법: ec2ctl <스크립트_이름> [환경_이름]
#   환경_이름을 지정하지 않으면 기본적으로 '.env' 파일을 사용합니다.
# 예시: ec2ctl connect # .env 파일을 사용하여 connect.sh 실행
#       ec2ctl open dev # dev.env 파일을 사용하여 open.sh 실행
ec2ctl() {
  local script_name="$1"
  local env_arg="$2"
  local project_dir="PROJECT_DIR_PLACEHOLDER" # install.sh 실행 시점의 프로젝트 경로가 여기에 삽입됩니다.

  if [[ -z "$script_name" ]]; then
    echo "사용법: ec2ctl <스크립트_이름> [환경_이름]"
    echo "  스크립트_이름: open, close, connect"
    echo "  환경_이름:    사용할 .env 파일의 이름 (예: dev, prod). 지정하지 않으면 '.env' 사용."
    return 1
  fi

  local script_path="${project_dir}/${script_name}.sh"
  local env_file="${env_arg}.env"

  local full_env_path="${project_dir}/envs/${env_file}"

  if [[ ! -f "$script_path" ]]; then
    echo "오류: 스크립트 '${script_name}.sh'를 찾을 수 없습니다: '${script_path}'"
    return 1
  fi

  if [[ ! -f "$full_env_path" ]]; then
    echo "오류: 환경 파일 '${env_file}'를 찾을 수 없습니다: '${full_env_path}'"
    return 1
  fi

  echo "실행 중: ${script_name}.sh (환경: ${env_file})..."
  "${script_path}" --env "${env_file}"
}
# --- End EC2 Control Scripts Function ---
EOF
)

# EC2CTL_FUNCTION 내의 PROJECT_DIR_PLACEHOLDER를 실제 PROJECT_DIR 값으로 대체
EC2CTL_FUNCTION="${EC2CTL_FUNCTION//PROJECT_DIR_PLACEHOLDER/${PROJECT_DIR}}"

# 셸 감지 및 해당 RC 파일 결정
SHELL_NAME=$(basename "$SHELL")
SHELL_RC_FILE=""

case "$SHELL_NAME" in
  "bash")
    SHELL_RC_FILE="$HOME/.bashrc"
    ;;
  "zsh")
    SHELL_RC_FILE="$HOME/.zshrc"
    ;;
  *)
    echo "경고: 지원되지 않는 셸 ($SHELL_NAME) 입니다. .bashrc 또는 .zshrc를 수동으로 확인해주세요."
    echo "함수를 추가할 셸 설정 파일을 지정해주세요 (예: ~/.bashrc, ~/.zshrc):"
    read -r SHELL_RC_FILE
    if [[ -z "$SHELL_RC_FILE" ]]; then
      echo "설치할 셸 설정 파일이 지정되지 않아 설치를 취소합니다."
      exit 1
    fi
    ;;
esac

if [[ ! -f "$SHELL_RC_FILE" ]]; then
  echo "경고: 셸 설정 파일 '$SHELL_RC_FILE'을 찾을 수 없습니다. 새로 생성하시겠습니까? (y/N)"
  read -p "새로 생성하시겠습니까? (y/N): " create_new_rc
  if [[ "$create_new_rc" == "y" || "$create_new_rc" == "Y" ]]; then
    touch "$SHELL_RC_FILE"
    echo "새로운 셸 설정 파일 '$SHELL_RC_FILE'을 생성했습니다."
  else
    echo "설치를 취소합니다."
    exit 1
  fi
fi


echo "----------------------------------------------------"
echo "EC2 제어 스크립트 함수를 '$SHELL_RC_FILE'에 추가합니다."
echo "이 작업은 셸 설정 파일을 수정합니다."
echo "----------------------------------------------------"

read -p "계속하시겠습니까? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "설치를 취소합니다."
  exit 1
fi

# 이미 함수가 존재하는지 확인
if grep -q "ec2ctl()" "$SHELL_RC_FILE"; then
  echo "경고: 'ec2ctl' 함수가 이미 '$SHELL_RC_FILE'에 존재합니다. 중복 추가를 건너뜁니다."
else
  printf "\n%s\n" "${EC2CTL_FUNCTION}" >> "$SHELL_RC_FILE"
  echo "성공적으로 'ec2ctl' 함수를 '$SHELL_RC_FILE'에 추가했습니다."
  echo "새로운 터미널을 열거나 'source $SHELL_RC_FILE'를 실행하여 적용하세요."
fi