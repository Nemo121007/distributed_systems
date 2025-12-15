FROM boinc/client:latest

# Установка Python и зависимостей
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
COPY ../app/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
USER boinc

# Копирование приложения
COPY ../app/iris_classifier.py /usr/local/bin/
RUN chmod +x /usr/local/bin/iris_classifier.py