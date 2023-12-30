import locust
from locust import HttpUser, TaskSet, task, between
from locust.contrib.fasthttp import FastHttpUser
# from locust.exceptions import StopLocust
# from locust.utils import get_random_string
import random

class MyTaskSet(TaskSet):
    def __init__(self):
        super(MyTaskSet, self).__init__(user_classes=[FastHttpUser])

    @task
    def my_task(self):
        # Get the parameter passed in the command line
        param = self.system_configuration.get_param("my_param")

        # Do something with the parameter
        print(f"Hello, {param}!")

    def set_params(self, params):
        # Set the parameter for the task
        self.system_configuration.set_param("my_param", params["my_param"])

class MyLocust(HttpUser):
    tasks = [MyTaskSet]

    def on_start(self):
        # Get the parameter passed in the command line
        param = super().system_configuration.get_param("my_param")
        # param = self.system_configuration.get_param("my_param")

        # Print the parameter
        print(f"Starting with param {param}")

if __name__ == "__main__":
    locust_args = ["--host=http://example.com", "--port=8080"]
    my_param = "some-value"
    locust.run(MyLocust, locust_args, my_param)