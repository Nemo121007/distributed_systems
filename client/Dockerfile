FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN pip3 install numpy scikit-learn

# Создание директорий
RUN mkdir -p /shared/work /shared/results

# Копируем приложение
COPY client_worker.py /app/client_worker.py

# Рабочая директория
WORKDIR /app

# Запуск приложения
CMD ["python3", "client_worker.py"]