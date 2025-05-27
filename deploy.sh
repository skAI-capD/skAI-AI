#!/bin/bash

APP_DIR="/home/ubuntu/diary-fastapi"

echo "📦 Moving to $APP_DIR"
cd $APP_DIR

echo "🔄 Pulling latest code"
git pull origin main

echo "💽 Activating virtualenv & installing dependencies"
source venv/bin/activate
pip install -r requirements.txt

echo "🔁 Restarting FastAPI"
pkill -f uvicorn
bash run.sh
