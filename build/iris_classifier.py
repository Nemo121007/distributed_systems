import sys
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def main():
    try:
        # Загрузка данных ирисов
        iris = load_iris()
        X = iris.data
        y = iris.target
        target_names = iris.target_names

        # Разделение на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        # Обучение модели
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Предсказание и оценка
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(
            y_test, y_pred, target_names=target_names, zero_division=0
        )

        # Формирование отчета
        output_lines = [
            "BOINC Iris Classification Test Report",
            "=====================================",
            f"Model: Random Forest (n_estimators=100)",
            f"Test Set Size: {len(y_test)} samples",
            f"Accuracy: {accuracy:.4f}",
            "",
            "Detailed Classification Report:",
            report
        ]

        # Запись отчета в файл
        output_file = "result.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(output_lines))

        print(f"Successfully generated report: {output_file}")
        print("\n".join(output_lines))

        # Успешное завершение
        sys.exit(0)

    except Exception as e:
        # Обработка ошибок
        error_message = f"ERROR: {str(e)}"
        print(error_message, file=sys.stderr)

        # Запись ошибки в файл
        try:
            with open("error.txt", 'w') as f:
                f.write(error_message)
        except:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()