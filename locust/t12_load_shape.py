from loguru import logger
from termcolor import colored

from locust import HttpUser, task, between

from locust import HttpUser, task, between
from locust.env import Environment
from locust import LoadTestShape


class MyUser(HttpUser):
    wait_time = between(4, 5)
    host = 'https://your-base-url.com'
    

    @task
    def my_task(self):
        logger.warning(colored("==>> my_task: my_task", "green"))
        # self.client.get("/")  # Make a GET request to the base URL

env = Environment(user_classes=[MyUser])
env.create_local_runner()
logger.warning(colored(f"==>> env.runner: {env.runner}", "green"))

# Определение типов тестов
      
class ConstantLoadShape(LoadTestShape):
    # def __init__(self, user_count=1):  # Provide a default value for user_count
    #     self.user_count = user_count

    def tick(self):
        return (self.user_count, self.user_count)

    
class RampUpLoadShape(LoadTestShape):
    def __init__(self, start_users=1, end_users=10, duration=60):  # Provide default values
        self.start_users = start_users
        self.end_users = end_users
        self.duration = duration
        self.current_time = 0

    def tick(self):
        if self.current_time >= self.duration:
            return None

        current_users = int(self.start_users + (self.end_users - self.start_users) * self.current_time / self.duration)
        self.current_time += 1
        return (current_users, current_users)

# Выбор типа теста из командной строки
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--test_type", choices=["constant", "ramp_up"], required=True)
    parser.add_argument("--user_count", type=int, default=5)
    parser.add_argument("--start-users", type=int, default=1)
    parser.add_argument("--end-users", type=int, default=7)
    parser.add_argument("--duration", type=int, default=1000)
    args = parser.parse_args()

    # env = Environment(user_classes=[MyUser])

    logger.warning(colored(f"==>> args.user_count: {args.user_count}", "green"))
    logger.warning(colored(f"==>> args.test_type: {args.test_type}", "green"))
    if args.test_type == "constant":
        if args.user_count is None:
            raise ValueError("Необходимо указать количество пользователей для постоянной нагрузки")
        load_shape = ConstantLoadShape()
        # load_shape = ConstantLoadShape(args.user_count)
    elif args.test_type == "ramp_up":
        if args.start_users is None or args.end_users is None or args.duration is None:
            raise ValueError("Необходимо указать начальное/конечное количество пользователей и длительность для нарастающей нагрузки")
        load_shape = RampUpLoadShape(args.start_users, args.end_users, args.duration)

    logger.warning(colored(f"==>> load_shape: {load_shape}", "green"))
    logger.warning(colored(f"==>> env: {env}", "green"))
    logger.warning(colored(f"==>> env.runner: {env.runner}", "green"))
    
    env.runner.start_shape()
    # env.runner.start_shape(load_shape)
    # env.runner.start(user_count=args.user_count, spawn_rate=1) #, user_classes=[MyUser])  # Adjust spawn_rate as needed
    # env.runner.start()
    # env.runner.start(load_shape=load_shape)
