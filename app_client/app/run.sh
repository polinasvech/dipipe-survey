#!/usr/bin/env bash
set -e

echo "Запуск приложения..."
export PYTHONPATH=/opt/app/app
python main.py
#uvicorn main:asgi_app --host 0.0.0.0 --port 8001 --reload