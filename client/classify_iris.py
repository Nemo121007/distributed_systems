#!/usr/bin/env python3
import os
import sys
import json
import time
import random
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from datetime import datetime


def create_status_file(client_id, status, progress=0):
    """Создает файл статуса для мониторинга"""
    status_data = {
        'client_id': client_id,
        'status': status,
        'progress': progress,
        'timestamp': datetime.now().isoformat()
    }

    status_file = f'/root/shared/results/client_{client_id}.status'
    with open(status_file, 'w') as f:
        json.dump(status_data, f, indent=2)


def main():
    # Получаем ID клиента из переменной окружения
    client_id = int(os.environ.get('CLIENT_ID', '0'))

    print(f"Starting iris classification for client {client_id}")

    # Создаем директорию для результатов
    os.makedirs('/root/shared/results', exist_ok=True)

    # Обновляем статус
    create_status_file(client_id, 'starting')

    try:
        # Имитация начала работы
        create_status_file(client_id, 'loading_data', 10)
        time.sleep(2)

        # Загружаем данные ирисов
        iris = load_iris()
        X = iris.data
        y = iris.target

        # Разделяем данные между клиентами
        if client_id == 0:
            # Первый клиент получает первые 75% данных
            split_idx = int(len(X) * 0.75)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
        else:
            # Второй клиент получает последние 75% данных
            split_idx = int(len(X) * 0.25)
            X_train, X_test = X[split_idx:], X[:split_idx]
            y_train, y_test = y[split_idx:], y[:split_idx]

        create_status_file(client_id, 'training', 30)
        time.sleep(2)

        # Обучаем модель
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        create_status_file(client_id, 'predicting', 70)
        time.sleep(2)

        # Делаем предсказания
        y_pred = model.predict(X_test)

        create_status_file(client_id, 'evaluating', 90)
        time.sleep(1)

        # Оцениваем точность
        accuracy = accuracy_score(y_test, y_pred)

        # Сохраняем модель
        model_filename = f'/root/shared/results/iris_model_client_{client_id}.pkl'
        joblib.dump(model, model_filename)

        # Сохраняем результаты
        results = {
            'client_id': client_id,
            'timestamp': datetime.now().isoformat(),
            'samples_processed': len(X_test),
            'accuracy': float(accuracy),
            'feature_importance': model.feature_importances_.tolist(),
            'test_indices': X_test.tolist(),
            'predictions': y_pred.tolist(),
            'actual': y_test.tolist(),
            'model_filename': model_filename
        }

        results_filename = f'/root/shared/results/results_client_{client_id}.json'
        with open(results_filename, 'w') as f:
            json.dump(results, f, indent=2)

        # Обновляем финальный статус
        create_status_file(client_id, 'completed', 100)

        print(f"Client {client_id} completed iris classification")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Samples processed: {len(X_test)}")
        print(f"Results saved to {results_filename}")

    except Exception as e:
        print(f"Error in client {client_id}: {str(e)}")
        create_status_file(client_id, 'error', 0)
        sys.exit(1)


if __name__ == "__main__":
    main()