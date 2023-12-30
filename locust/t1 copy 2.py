from locust import HttpUser, task, events, between, run_single_user


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--my-argument", type=str, env_var="LOCUST_MY_ARGUMENT", default="", help="It's working")
    # Choices will validate command line input and show a dropdown in the web UI
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev", help="Environment")
    # Set `include_in_web_ui` to False if you want to hide from the web UI
    parser.add_argument("--my-ui-invisible-argument", include_in_web_ui=False, default="I am invisible")
    # Set `is_secret` to True if you want the text input to be password masked in the web UI
    parser.add_argument("--my-ui-password-argument", is_secret=True, default="I am a secret")


@events.test_start.add_listener
def _(environment, **kw):
    print(f"Custom argument supplied: {environment.parsed_options.my_argument}")


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    host = 'd'
    
    @task
    def my_task(self):
        print(f"my_argument={self.environment.parsed_options.my_argument}")
        print(f"my_argument={self.environment.parsed_options.env}")
        print(f"my_ui_invisible_argument={self.environment.parsed_options.my_ui_invisible_argument}")

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(WebsiteUser)        