#!/usr/bin/env python3
import json
import os
from datetime import datetime


def main():
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

    print(f"\n=== COMBINED RESULTS ===")
    print(f"Total samples processed: {total_samples}")
    print(f"Total correct predictions: {total_correct}")
    print(f"Overall accuracy: {overall_accuracy:.4f}")
    print(f"Results saved to: {results_dir}/combined_results.json")


if __name__ == "__main__":
    main()