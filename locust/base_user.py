from loguru import logger
from termcolor import colored

from locust import HttpUser, between, task

class BaseUser(HttpUser):
    wait_time = between(2, 2)  # wait time between requests

    def on_start(self):
        # код, который выполняется при старте теста
        pass

    def on_stop(self):
        # код, который выполняется при остановке теста
        pass
    
    @task
    def index_page(self):
        logger.warning(colored(f"==>> {self.__class__.__name__}: BaseUser" , color="green"))

