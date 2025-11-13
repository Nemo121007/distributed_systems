import os
import time
import sys
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def process_task(task_file):
    """Обрабатывает задание от сервера"""
    try:
        # Проверяем, что файл существует
        if not os.path.exists(task_file):
            print(f"Task file does not exist: {task_file}")
            return False

        # Читаем задание
        with open(task_file, 'r') as f:
            task_content = f.read().strip()

        print(f"Processing task: {os.path.basename(task_file)}")

        # Выполняем классификацию ирисов
        iris = load_iris()
        X = iris.data
        y = iris.target
        target_names = iris.target_names

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(
            y_test, y_pred, target_names=target_names, zero_division=0
        )

        # Формируем отчет
        output_lines = [
            f"Task: {os.path.basename(task_file)}",
            "BOINC Iris Classification Test Report",
            "=====================================",
            f"Model: Random Forest (n_estimators=100)",
            f"Test Set Size: {len(y_test)} samples",
            f"Accuracy: {accuracy:.4f}",
            "",
            "Detailed Classification Report:",
            report
        ]

        # Создаем файл результата
        result_file = f"/shared/results/{os.path.basename(task_file).replace('.wu', '.result')}"
        with open(result_file, 'w') as f:
            f.write("\n".join(output_lines))

        print(f"Result saved to: {result_file}")

        # Удаляем задание после обработки
        os.remove(task_file)
        print(f"Removed task file: {task_file}")

        return True
    except Exception as e:
        print(f"Error processing task {task_file}: {str(e)}", file=sys.stderr)
        return False


def main():
    # Ждем 10 секунд, чтобы сервер успел создать задания
    print("Client worker started. Waiting for server to create tasks...")
    time.sleep(10)

    work_dir = "/shared/work"

    # Проверяем, что директория существует
    if not os.path.exists(work_dir):
        print(f"Directory {work_dir} does not exist!")
        return

    print(f"Client worker started, monitoring {work_dir}")

    while True:
        try:
            # Проверяем наличие заданий
            if os.path.exists(work_dir):
                task_files = [f for f in os.listdir(work_dir) if f.endswith('.wu')]
                print(f"Found task files: {task_files}")

                if task_files:
                    for task_file in task_files:
                        full_path = os.path.join(work_dir, task_file)
                        print(f"Processing task: {full_path}")
                        process_task(full_path)
                else:
                    print("No tasks found, waiting...")
            else:
                print(f"Work directory {work_dir} does not exist, waiting...")

            # Проверяем каждые 5 секунд
            time.sleep(5)
        except Exception as e:
            print(f"Error in client worker: {str(e)}", file=sys.stderr)
            time.sleep(10)


if __name__ == "__main__":
    main()