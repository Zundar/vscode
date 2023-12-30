from locust import HttpUser, task, between

class MyUser(HttpUser):
    host = 'd'
    wait_time = between(1, 2.5)

    @task
    def my_task(self):
        user_count = self.environment.runner.user_count
        print(f"Текущее количество вузеров: {user_count}")

        # ваша логика выполнения задачи

