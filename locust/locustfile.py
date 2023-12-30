# В файле locustfile.py

from locust import HttpUser, task, between
from load_test_shape import MyLoadTestShape
from locust.main import main
import sys


class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = 'd'

    @task
    def my_task(self):
        # Ваша логика выполнения задачи
        print(f'{self.environment.runner.user_count}')
        pass
# изменим способ передачи параметров в LoadTestShape. Вместо передачи параметров через конструктор, 
# воспользуемся атрибутами класса для хранения параметров и методом класса для их установки.
# Теперь параметры хранятся в атрибутах класса MyLoadTestShape, и метод set_params позволяет устанавливать их из скрипта
# Задаем параметры для MyLoadTestShape
MyLoadTestShape.set_params('stab', 5, 2)

# Запуск Locust из скрипта
if __name__ == "__main__":
    sys.argv = [
        "--headless",
        "--headless",
        "--only-summary",
        "-f", __file__,
    ]

    main()
