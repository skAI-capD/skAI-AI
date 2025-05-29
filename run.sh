#!/bin/bash

echo "🟢 Starting FastAPI server..."
cd ~/diary-fastapi
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8081 > server.log 2>&1 &
echo "✅ Server started"