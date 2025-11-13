#!/bin/bash

# Создаем директорию build, если ее нет
mkdir -p build

# Копируем исходный код в директорию сборки
cp iris_classifier.py build/

# Собираем образ для сборки приложения
docker build -t iris-builder build/

# Создаем временный контейнер и копируем собранный файл
docker create --name extract-iris iris-builder
docker cp extract-iris:/app/dist/iris_classifier_app ./client/
docker rm extract-iris

# Делаем файл исполняемым
chmod +x ./client/iris_classifier_app

echo "Сборка завершена. Исполняемый файл скопирован в ./client/"