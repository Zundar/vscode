# В файле locustfile.py

from locust import HttpUser, task, between
from locust.main import main
from load_test_shape import MyLoadTestShape

import sys

class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = 'd'

    @task
    def my_task(self):
        # Ваша логика выполнения задачи
        print(f'{self.environment.runner.user_count}')
        pass

if __name__ == "__main__":
    # Получение параметров из командной строки
    user_count_param = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    spawn_rate_param = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    # Установка параметров для MyLoadTestShape
    MyLoadTestShape.set_params('dd', user_count_param, spawn_rate_param)

# Запуск Locust из скрипта
if __name__ == "__main__":
    sys.argv = [
        "--headless",
        "--headless",
        "--only-summary",
        "-f", __file__,
    ]

    main()
