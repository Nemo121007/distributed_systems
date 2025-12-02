#!/bin/bash

echo "=== Starting BOINC Client Debug ==="

# Ожидание готовности сервера
echo "Waiting for BOINC server to be ready..."
while ! nc -z boinc-server-docker-apache-1 80; do
    sleep 1
done

echo "BOINC server is ready!"

# Инициализация директории BOINC клиента
echo "Initializing BOINC client directories..."
mkdir -p /var/lib/boinc
mkdir -p /var/log/boinc

# Создание конфигурационного файла
echo "Creating configuration file..."
cat > /var/lib/boinc/cc_config.xml << 'CONFIG'
<cc_config>
    <log_dir>/var/log/boinc</log_dir>
    <max_file_xfers>3</max_file_xfers>
    <max_file_xfers_per_project>2</max_file_xfers_per_project>
    <disallow_attach>0</disallow_attach>
</cc_config>
CONFIG

# Проверим, доступен ли BOINC бинарный файл
echo "Checking BOINC binary..."
which boinc
echo "BOINC version:"
boinc --version

# Создадим пустой файл лога и дадим права на запись
echo "Creating empty log file..."
touch /var/log/boinc/boinc.log
chmod 666 /var/log/boinc/boinc.log

# Запустим BOINC клиент в foreground режиме с явным указанием лог-файла
echo "Starting BOINC client in foreground mode..."
boinc --dir /var/lib/boinc --redirectio &
BOINC_PID=$!

echo "BOINC started with PID: $BOINC_PID"

# Дадим время на запуск
sleep 5

# Проверим, работает ли процесс
if ps -p $BOINC_PID > /dev/null; then
    echo "BOINC process is running"
    
    # Проверим содержимое лог-файла
    echo "Checking log file contents:"
    if [ -s /var/log/boinc/boinc.log ]; then
        cat /var/log/boinc/boinc.log
    else
        echo "Log file is empty"
    fi
    
    # Держим контейнер запущенным и следим за процессом BOINC
    echo "Keeping container alive and monitoring BOINC process..."
    while true; do
        if ! ps -p $BOINC_PID > /dev/null; then
            echo "BOINC process has stopped. Exiting..."
            exit 1
        fi
        sleep 30
        echo "BOINC process is still running (PID: $BOINC_PID)"
    done
else
    echo "Failed to start BOINC process"
    exit 1
fi