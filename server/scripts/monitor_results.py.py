#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime


def monitor_results():
    """Мониторинг результатов от клиентов"""
    results_dir = '/results'
    status_file = f'{results_dir}/status.json'

    while True:
        try:
            # Собираем информацию о результатах
            status = {
                'timestamp': datetime.now().isoformat(),
                'clients': {},
                'total_jobs': 0,
                'completed_jobs': 0
            }

            # Проверяем наличие результатов
            if os.path.exists(results_dir):
                for filename in os.listdir(results_dir):
                    if filename.startswith('results_client_') and filename.endswith('.json'):
                        client_id = filename.split('_')[2].split('.')[0]

                        with open(os.path.join(results_dir, filename), 'r') as f:
                            client_result = json.load(f)

                        status['clients'][client_id] = {
                            'status': 'completed',
                            'accuracy': client_result.get('accuracy', 0),
                            'samples_processed': client_result.get('samples_processed', 0),
                            'timestamp': client_result.get('timestamp', 'unknown')
                        }
                        status['completed_jobs'] += 1
                    elif filename.startswith('client_') and filename.endswith('.status'):
                        client_id = filename.split('_')[1].split('.')[0]
                        status['clients'][client_id] = {
                            'status': 'working',
                            'progress': 'unknown'
                        }

            status['total_jobs'] = 2  # У нас 2 клиента

            # Сохраняем статус
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)

            # Выводим информацию в консоль
            print(f"\n=== Status Update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
            print(f"Total jobs: {status['total_jobs']}")
            print(f"Completed jobs: {status['completed_jobs']}")

            for client_id, client_status in status['clients'].items():
                print(f"Client {client_id}: {client_status['status']}")
                if 'accuracy' in client_status:
                    print(f"  Accuracy: {client_status['accuracy']:.4f}")

            # Если все задания выполнены, объединяем результаты
            if status['completed_jobs'] == status['total_jobs']:
                print("\nAll jobs completed! Combining results...")
                combine_results()
                break

        except Exception as e:
            print(f"Error monitoring results: {e}")

        time.sleep(10)  # Проверяем каждые 10 секунд


def combine_results():
    """Объединение результатов от всех клиентов"""
    results_dir = '/results'
    combined_results = {
        'timestamp': datetime.now().isoformat(),
        'clients': {},
        'summary': {}
    }

    total_samples = 0
    total_correct = 0

    # Собираем результаты от клиентов
    for client_id in [0, 1]:
        filename = f'{results_dir}/results_client_{client_id}.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                client_result = json.load(f)

            combined_results['clients'][f'client_{client_id}'] = client_result
            total_samples += client_result.get('samples_processed', 0)

            # Подсчитываем правильные предсказания
            predictions = client_result.get('predictions', [])
            actual = client_result.get('actual', [])
            correct = sum(1 for p, a in zip(predictions, actual) if p == a)
            total_correct += correct

    # Вычисляем общую точность
    if total_samples > 0:
        overall_accuracy = total_correct / total_samples
    else:
        overall_accuracy = 0

    combined_results['summary'] = {
        'total_samples': total_samples,
        'total_correct': total_correct,
        'overall_accuracy': overall_accuracy
    }

    # Сохраняем объединенные результаты
    with open(f'{results_dir}/combined_results.json', 'w') as f:
        json.dump(combined_results, f, indent=2)

    print(f"\n=== FINAL RESULTS ===")
    print(f"Total samples processed: {total_samples}")
    print(f"Total correct predictions: {total_correct}")
    print(f"Overall accuracy: {overall_accuracy:.4f}")
    print(f"Results saved to: {results_dir}/combined_results.json")


if __name__ == "__main__":
    monitor_results()