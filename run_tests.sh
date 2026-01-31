#!/usr/bin/env bash
set -e

export PYTHONPATH=src


if ! command -v python3 &> /dev/null; then
  echo "❌ python3 не найден. Установи Python 3.10+"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "📦 Создаю виртуальное окружение..."
  python3 -m venv .venv
fi

echo "🐍 Активирую venv"
source .venv/bin/activate

echo "⬆️ Обновляю pip"
pip install --upgrade pip

echo "📚 Устанавливаю зависимости"
pip install -r requirements-tests.txt

echo "🧪 Запускаю unit-тесты"
pytest tests/unit -v

echo "✅ Все unit-тесты прошли успешно"
