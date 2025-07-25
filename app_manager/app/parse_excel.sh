#!/usr/bin/env bash
set -e

export PYTHONPATH=/opt/app/app

echo "Запуск парсинга xlsx..."
python parse_excel.py