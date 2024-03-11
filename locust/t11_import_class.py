from loguru import logger
from termcolor import colored

from locust import HttpUser, task, between
from t11_import_class2 import MyThirdHttpUser
import log

class MyHttpUser(HttpUser):
    wait_time = between(1, 5)  # wait time between requests
    host = "https://example.com"  # base URL for HTTP requests

    @task
    def index_page(self):
        logger.warning(colored(f"==>> {self.__class__.__name__}: MyHttpUser" , color="green"))

class MySecondHttpUser(HttpUser):
    wait_time = between(2, 6)  # wait time between requests
    host = "https://example.com"  # base URL for HTTP requests

    @task
    def login(self):
        logger.warning(colored(f"==>> {self.__class__.__name__}: MySecondHttpUser", "yellow"))

# Use the imported class
class MyFourthHttpUser(MyThirdHttpUser):
    weight = 2

if __name__ == "__main__":
    import sys
    from locust.main import main
    # sys.argv = ['locust', '-f', __file__, '--headless', '-u', '10', '-r', '10', '-t', '1m', '--only-summary']
    sys.argv = ['locust', '-f', __file__, '--headless', '-u', '10', '-r', '10', '-t', '1m', '--only-summary', 'MyFourthHttpUser', 'MyHttpUser']
    main()
# locust -f __file__ --headless -u 1 -r 10 -t 1m --only-summary MyThirdHttpUser