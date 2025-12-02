#!/usr/bin/env python3
import subprocess
import os
import json
import time
from datetime import datetime


def wait_for_server():
    """Ожидание готовности сервера"""
    print("Waiting for BOINC server to be ready...")
    while True:
        try:
            result = subprocess.run(['bin/status'], capture_output=True, text=True)
            if result.returncode == 0:
                print("BOINC server is ready!")
                break
        except:
            pass
        time.sleep(5)


def create_iris_jobs():
    """Создание заданий для классификации ирисов"""
    print("Creating iris classification jobs...")

    # Создаем задания для двух клиентов
    for client_id in [0, 1]:
        print(f"Creating job for client {client_id}")

        # Создаем задание с использованием Docker-образа
        cmd = [
            'bin/boinc2docker_create_work.py',
            'boinc-iris-client:latest',
            'python', '/app/classify_iris.py'
        ]

        # Устанавливаем переменные окружения
        env = os.environ.copy()
        env['CLIENT_ID'] = str(client_id)
        env['WORKUNIT_NAME'] = f'iris_client_{client_id}_{int(time.time())}'

        # Запускаем создание задания
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Job for client {client_id} created successfully")
        else:
            print(f"✗ Error creating job for client {client_id}")
            print(f"Error: {result.stderr}")


def main():
    # Переходим в директорию проекта
    os.chdir('/home/boincadm/project')

    # Ожидаем готовности сервера
    wait_for_server()

    # Создаем задания
    create_iris_jobs()

    print("\nJobs created successfully!")
    print("Monitor the progress at: http://localhost:8080")


if __name__ == "__main__":
    main()