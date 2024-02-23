from locust import User, task, between

class MyUser(User):
    wait_time = between(1, 2)
    
    def execute_task(self, task, *args, **kwargs):
        task_name = task.__name__
        print(f"Starting task: {task_name}")
        task(self, *args, **kwargs)
    
    @task
    def my_task(self):
        print("Doing my_task")
    
    @task
    def another_task(self):
        print("Doing another_task")

if __name__ == "__main__":
    import sys
    from locust.main import main
    sys.argv = ['locust', '-f', __file__, '--headless', '-u', '1', '-r', '10', '-t', '1m', '--only-summary']
    main()
