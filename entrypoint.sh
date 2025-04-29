#!/bin/sh
while true; do
  echo "Привет родной!"
    python manage.py runserver 0.0.0.0:8000
    echo "Ошибка! Перезапуск через 5 секунд..."
    sleep 5
done
