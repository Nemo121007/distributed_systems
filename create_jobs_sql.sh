#!/bin/bash

# Скрипт для создания заданий через SQL с правильными учетными данными
docker exec boinc-server-docker-apache-1 mysql -h mysql -u root -ppassword boincserver << 'SQL_EOF'
INSERT INTO workunit (create_time, appid, name, command_line, input_template, result_template) 
VALUES (NOW(), 1, 'iris_client_1', 'python /app/classify_iris.py', '<file_info>', '<file_info>');

INSERT INTO workunit (create_time, appid, name, command_line, input_template, result_template) 
VALUES (NOW(), 1, 'iris_client_2', 'python /app/classify_iris.py', '<file_info>', '<file_info>');

SELECT id, name, create_time FROM workunit ORDER BY create_time DESC LIMIT 10;
SQL_EOF
