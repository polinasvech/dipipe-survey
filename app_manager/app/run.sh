#!/usr/bin/env bash
set -e

echo "Запуск парсинга xlsx..."
export PYTHONPATH=/opt/app/app
#python parse_excel.py
uvicorn main:app --host 0.0.0.0 --port 8002 --reload