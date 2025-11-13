import os
import time
import shutil
from datetime import datetime


def main():
    # Создаем директории, если их нет
    os.makedirs("/shared/work", exist_ok=True)
    os.makedirs("/shared/results", exist_ok=True)
    os.makedirs("/shared/processed", exist_ok=True)

    print("Work generator started...")

    try:
        while True:
            # Создаем 2 новых задания
            for i in range(2):
                work_unit_id = f"wu_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                task_file = f"/shared/work/{work_unit_id}.wu"

                # Создаем файл задания
                with open(task_file, "w") as f:
                    f.write("iris_classification_task")

                print(f"Created work unit: {work_unit_id}")
                print(f"File path: {task_file}")
                print(f"File exists: {os.path.exists(task_file)}")

                # Проверяем содержимое директории
                print(f"Contents of /shared/work: {os.listdir('/shared/work')}")

            # Обрабатываем полученные результаты
            results_dir = "/shared/results"
            if os.path.exists(results_dir):
                for result_file in os.listdir(results_dir):
                    if result_file.endswith(".result"):
                        try:
                            with open(os.path.join(results_dir, result_file), 'r') as f:
                                content = f.read()
                                print(f"\n=== Received result from {result_file} ===")
                                print(content)
                                print("=" * 50)

                            # Перемещаем обработанный результат в архив
                            shutil.move(
                                os.path.join(results_dir, result_file),
                                f"/shared/processed/{result_file}"
                            )
                        except Exception as e:
                            print(f"Error processing result {result_file}: {str(e)}")

            # Ждем 30 секунд перед созданием новых заданий
            time.sleep(2)
    except KeyboardInterrupt:
        print("Work generator stopped.")
    except Exception as e:
        print(f"Error in work generator: {str(e)}")


if __name__ == "__main__":
    main()