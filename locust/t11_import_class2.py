from loguru import logger
from termcolor import colored

from locust import HttpUser, task, between

class MyThirdHttpUser(HttpUser):
    wait_time = between(2, 5)  # wait time between requests
    host = "https://myapp.com"  # base URL for HTTP requests

    @task
    def search(self):
        # print(f"{self.__class__.__name__}: MyThirdHttpUser")
        logger.warning(colored(f"==>> {self.__class__.__name__}: MyThirdHttpUser", "red"))
        # logger.warning(colored(f"==>> dir(self.environment.runner): {dir(self.environment.runner)}", "green"))
        logger.warning(colored(f"==>> self.environment.runner.user_classes: {self.environment.runner.target_user_classes_count}", "green"))
if __name__ == "__main__":
    import sys
    from locust.main import main
    sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '--only-summary']
    # sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '--only-summary', 'MyThirdHttpUser']
    # sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '-t', '1m', '--only-summary', 'MyThirdHttpUser']
    main()