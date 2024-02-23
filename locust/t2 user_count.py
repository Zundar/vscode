from locust import HttpUser, task, between, run_single_user

class MyUser(HttpUser):
    wait_time = between(1, 2.5)

    host = 'd'

    @task
    def my_task(self):
        print(f"Current user count: {self.environment.runner.user_count}")

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(MyUser)        