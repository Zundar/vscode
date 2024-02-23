import os
from locust import HttpUser, task, between, run_single_user


class MyUser(HttpUser):
    wait_time = between(1, 2)
    host = 'd'

    @task
    def my_task(self):
        print(os.path.basename(__file__))

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(MyUser)        