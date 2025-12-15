#!/bin/bash
set -e

# Даем время на инициализацию сети
echo "Waiting for network initialization..."
sleep 20

# Используем статический IP базы данных из переменной окружения
DB_IP=${DB_HOST}
echo "Database IP: $DB_IP"

# Ожидание доступности базы данных
echo "Waiting for database connection..."
until nc -z $DB_IP 3306; do
  echo "Waiting for database connection at $DB_IP..."
  sleep 5
done

# Инициализация проекта
if [ ! -d "/var/lib/boinc/iris_project" ]; then
    cd /var/lib/boinc
    echo "Creating BOINC project..."
    # Используем make_project из установленного BOINC
    /opt/boinc/make_project --url_base http://localhost:80 --db_user root --db_passwd boinc --db_host $DB_IP iris_project
fi

# Запуск BOINC-сервера
cd /var/lib/boinc/iris_project
echo "Starting BOINC server..."
./bin/start --daemon

# Запуск Apache
echo "Starting Apache..."
apache2ctl -D FOREGROUND