from locust import HttpUser, LoadTestShape, task, between
from locust.env import Environment
from loguru import logger
from termcolor import colored

class WebsiteUser(HttpUser):
    wait_time = between(2, 3)
    host='www.example.com'

    @task
    def view_item(self):
        logger.warning(colored(f"==>> view_item: ", "green"))
        # self.client.get("/item")

class ConstantUserLoadTest(LoadTestShape):
    user_classes = {WebsiteUser: 1}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_user_count = 2
        self.spawn_rate = 10
        logger.warning(colored(f"==>> ConstantUserLoadTest: {ConstantUserLoadTest}", "green"))

    def tick(self):
        logger.warning(colored(f"==>> ConstantUserLoadTest: {ConstantUserLoadTest}", "green"))
        pass
        return self.target_user_count, self.spawn_rate

class RampUpUserLoadTest(LoadTestShape):
    user_classes = {WebsiteUser: 1}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spawn_rate = 10
        self.target_user_count = 100
        logger.warning(colored(f"==>> RampUpUserLoadTest: {RampUpUserLoadTest}", "green"))

    def tick(self):
        logger.warning(colored(f"==>> RampUpUserLoadTest: {RampUpUserLoadTest}", "green"))
        run_time = self.get_run_time()

        if run_time < 30:
            # Ramp up users for the first 30 seconds
            self.spawn_rate = 10
            self.target_user_count = run_time / 2
        elif run_time < 60:
            # Keep a constant number of users for 30 seconds
            self.spawn_rate = 0
            self.target_user_count = 60
        else:
            # Ramp down users for the remaining time
            self.spawn_rate = -10
            self.target_user_count = 120 - (run_time - 60) * 2

        return self.target_user_count, self.spawn_rate
    
if __name__ == "__main__":
    import sys
    from locust.main import main
    import log

    sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '--only-summary', '--host', 'www.example.com']
    # logger.warning(colored(f"==>> sys.argv: {sys.argv}", "green"))
    shape_class = ConstantUserLoadTest()  # создаем экземпляр класса ConstantUserLoadTest
    # shape_class = ConstantUserLoadTest()  # создаем экземпляр класса ConstantUserLoadTest
    environment = Environment(user_classes=[WebsiteUser], shape_class=shape_class)  # передаем экземпляр класса ConstantUserLoadTest в качестве аргумента shape_class
    logger.warning(colored(f"==>> environment.parsed_options: {environment.parsed_options}", "green"))
    environment.create_local_runner()
    # environment.runner.start(1, 2)
    main()
