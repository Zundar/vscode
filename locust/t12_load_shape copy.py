from locust import LoadTestShape, User, task, between, HttpUser, TaskSet
from locust.env import Environment
from locust.runners import LocalRunner
import argparse

class MyTaskSet(TaskSet):
    @task
    def index(self):
        self.client.get("/")

class MyUser(HttpUser):
    tasks = [MyTaskSet]
    wait_time = between(1, 2)

class LoadShape1(LoadTestShape):
    def tick(self):
        return (1, 1)

class LoadShape2(LoadTestShape):
    def tick(self):
        return (2, 2)

parser = argparse.ArgumentParser()
parser.add_argument("--shape", type=int, default=1, 
                    help="LoadTestShape: 1 или 2")
args = parser.parse_args()

if args.shape == 1:
    load_shape_class = LoadShape1
elif args.shape == 2:
    load_shape_class = LoadShape2
else:
    print(f"Недопустимый выбор LoadTestShape: {args.shape}")
    exit(1)

env = Environment(user_classes=[MyUser])
env.create_local_runner()

env.runner.start_shape()

try:
    # ваши действия или команды чтобы запустить тест
    env.runner.greenlet.join()
finally:
    env.runner.quit()
