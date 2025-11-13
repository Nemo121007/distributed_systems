FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей (для возможных зависимостей времени выполнения)
RUN pip3 install numpy scikit-learn

# Копируем приложение
COPY iris_classifier_app /usr/local/bin/

# Делаем исполняемым
RUN chmod +x /usr/local/bin/iris_classifier_app

# Рабочая директория
WORKDIR /tmp

# Запуск приложения
CMD ["/usr/local/bin/iris_classifier_app"]