import os
from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = 'd'

    @task
    def my_task(self):
        print(os.path.basename(__file__))
