from locust import HttpUser, TaskSet, task, User, between
from locust.main import main
import sys

from locust import HttpUser, TaskSet, task

class MyTaskSet(TaskSet):
    @task
    def my_task(self):
        # Доступ к self.environment
        print("Accessing environment: %r" % self.user.environment.runner.user_count)

class MyUser(User):
    wait_time = between(5, 15)
    tasks = [MyTaskSet]

# Запуск Locust из скрипта
if __name__ == "__main__":
    sys.argv = [
        "--headless",
        "--headless",
        "--only-summary",
        "-f", __file__,
    ]

    main()
