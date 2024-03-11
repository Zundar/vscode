from loguru import logger
from termcolor import colored

from locust import HttpUser, between, task

from base_user import BaseUser

class MyUser(BaseUser):
    host = "https://example.com"
    wait_time = between(2, 2)  # wait time between requests


    @task
    def index_page2(self):
        logger.warning(colored(f"==>> {self.__class__.__name__}: MyUser" , color="green"))
        logger.warning(colored(f"==>> self.environment.runner.user_classes: {self.environment.runner.target_user_classes_count}", "green"))


if __name__ == "__main__":
    import sys
    from locust.main import main
    sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '-t', '1m', '--only-summary', '--host', 'https://example.com', 
                # 'MyUser'
                ]
    main()


