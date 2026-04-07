#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
  echo "Ошибка: запустите через sudo"
  exit 1
fi

CONF_NAME="LMS.conf"
SOURCE="./nginx.conf"
DEST_AVAIL="/etc/nginx/sites-available/$CONF_NAME"
DEST_ENABL="/etc/nginx/sites-enabled/$CONF_NAME"

echo "--- Обновление конфигурации $CONF_NAME ---"

if [ ! -f "$SOURCE" ]; then
    echo "Ошибка: Файл $SOURCE не найден в папке с репозиторием!"
    exit 1
fi

cp "$SOURCE" "$DEST_AVAIL"
echo "Конфиг скопирован в $DEST_AVAIL"

if [ ! -L "$DEST_ENABL" ]; then
    ln -s "$DEST_AVAIL" "$DEST_ENABL"
    echo "Ссылка в sites-enabled создана"
fi

echo "--- Тестирование Nginx ---"
nginx -t && systemctl reload nginx

if [ $? -eq 0 ]; then
    echo "Новый конфиг установлен"
else
    echo "Ошибка в конфиге! Проверь nginx.conf"
fi