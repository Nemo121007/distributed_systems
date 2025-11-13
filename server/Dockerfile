FROM ubuntu:22.04

# Установка базовых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN pip3 install numpy scikit-learn

# Создание директории проекта
RUN mkdir -p /var/lib/boinc/projects/iris

# Копирование файлов
COPY app_info.xml /var/lib/boinc/projects/iris/
COPY work_generator.py /var/lib/boinc/projects/iris/

# Рабочая директория
WORKDIR /var/lib/boinc/projects/iris

# Запуск генератора заданий
CMD ["python3", "work_generator.py"]