import os
import time
from datetime import datetime

def create_work_unit():
    work_unit_id = f"wu_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with open(f"/var/lib/boinc/projects/iris/{work_unit_id}.wu", "w") as f:
        f.write("iris_classification_task")
    return work_unit_id

if __name__ == "__main__":
    print("Work generator started...")
    while True:
        for i in range(2):  # Создаем 2 задания
            wu = create_work_unit()
            print(f"Created work unit: {wu}")
        time.sleep(10)  # Новые задания каждые 30 секунд
