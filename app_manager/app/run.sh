#!/usr/bin/env bash
set -e

export PYTHONPATH=/opt/app/app

echo "Запуск приложения..."
uvicorn main:app --host 0.0.0.0 --port 8002 --reload