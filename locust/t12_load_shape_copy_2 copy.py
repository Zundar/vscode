from locust import HttpUser, task, between, events
from locust.env import Environment
from locust.runners import MasterRunner

class MyUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def my_task(self):
        self.client.get("/")  # Замените на ваш запрос

# Set the load type here directly
load_test_type = "constant"  # Change to "step" for step load

def on_hatch_complete(environment, **kwargs):
    runner = environment.runner
    # ... your logic to set user_count and spawn_rate ...

# Create an Environment instance
environment = Environment(user_classes=[MyUser]) 

if load_test_type == "step":
    # Parameters for step load
    # ... (Inside the loop) ...
    events.hatch_complete.add_listener(lambda **kw: on_hatch_complete(environment, **kw))
    # ... 

else:
    # Constant load
    runner = MasterRunner(environment, master_bind_host="*", master_bind_port=5557)
    environment.runner = runner  
    on_hatch_complete(environment) 
    runner.start(50, spawn_rate=10)  # Start 50 users with spawn rate 10

environment.runner.run(300) 