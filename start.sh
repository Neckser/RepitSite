#!/bin/bash

# Останавливаем старые контейнеры (если есть)
docker compose down

# Собираем и запускаем
docker compose build
docker compose up -d

# Показываем статус
echo ""
echo "Контейнеры запущены:"
docker compose ps

# Показываем логи в реальном времени (опционально)
echo ""
echo "Логи приложения (Ctrl+C для выхода):"
docker compose logs -f app