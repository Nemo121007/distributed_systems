FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN pip3 install numpy scikit-learn

# Создание директорий
RUN mkdir -p /shared/work /shared/results /shared/processed

# Копирование файлов
COPY work_generator.py /app/work_generator.py

# Рабочая директория
WORKDIR /app

# Запуск генератора заданий
CMD ["python3", "work_generator.py"]