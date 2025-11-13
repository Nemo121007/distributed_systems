FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN pip3 install numpy scikit-learn pyinstaller

# Рабочая директория
WORKDIR /app

# Копируем исходный код
COPY iris_classifier.py .

# Компилируем приложение
RUN pyinstaller --onefile --name iris_classifier_app iris_classifier.py