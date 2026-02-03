#!/usr/bin/env bash
set -e

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
  echo "❌ Docker не найден. Установи Docker"
  exit 1
fi

# Собираем тестовый контейнер
echo "🐳 Сборка тестового Docker контейнера..."
sudo docker build -f Dockerfile.tests -t repitsite-tests .

# Запускаем тесты
echo "🧪 Запуск unit-тестов в контейнере..."
sudo docker run --rm repitsite-tests

echo "✅ Все тесты прошли"
