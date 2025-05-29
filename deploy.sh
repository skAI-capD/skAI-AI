#!/bin/bash

set -e  # ❗오류 발생 시 스크립트 즉시 중단 (안전장치)

APP_DIR="/home/ubuntu/diary-fastapi"

echo "📦 Moving to $APP_DIR"
cd "$APP_DIR" || { echo "❌ Directory $APP_DIR does not exist"; exit 1; }

echo "🔄 Pulling latest code from main"
git pull origin main || { echo "❌ Git pull failed"; exit 1; }

echo "💽 Activating virtualenv & installing dependencies"
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "❌ Virtualenv not found. You may need to run python -m venv venv"
  exit 1
fi

pip install --upgrade pip
pip install -r requirements.txt

echo "🔁 Restarting FastAPI"
pkill -f uvicorn || echo "No uvicorn process to kill"

bash run.sh
