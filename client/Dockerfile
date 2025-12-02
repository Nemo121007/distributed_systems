FROM boinc/client:latest

# Устанавливаем Python и необходимые зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    netcat-openbsd \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Обновляем pip до последней версии
RUN pip install --upgrade pip

# Устанавливаем Python-библиотеки в виртуальное окружение
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Копируем приложение
COPY classify_iris.py /app/classify_iris.py

# Создаем директорию для результатов
RUN mkdir -p /root/shared/results

# Копируем скрипт запуска и устанавливаем права
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаем символическую ссылку для результатов
RUN ln -sf /root/shared/results /app/results

# Создаем директорию для логов BOINC
RUN mkdir -p /var/log/boinc