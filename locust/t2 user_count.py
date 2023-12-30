from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2.5)

    host = 'd'

    @task
    def my_task(self):
        print(f"Current user count: {self.user_count}")