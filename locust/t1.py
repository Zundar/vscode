import logging
import sys
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
    # log = logging.getLogger()
    # log.setLevel(logging.INFO)

    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # fh = logging.FileHandler('locustfile.log')
    # fh.setLevel(logging.INFO)
    # fh.setFormatter(formatter)
    # log.addHandler(fh)

    # # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter)
    # log.addHandler(ch)
    
    # file_handler = logging.FileHandler(filename='tmp.log')
    # stdout_handler = logging.StreamHandler(stream=sys.stdout)
    # handlers = [file_handler, stdout_handler]

    # logging.basicConfig(
    #     level=logging.DEBUG, 
    #     format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    #     handlers=handlers
    # )

    import os
    print(os.path.basename(__file__))

    file_log = logging.FileHandler('tmp.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S', 
                    level=logging.DEBUG)

    log = logging.getLogger()
    logging.info('Info message')    
    
    log.warn("Fetch Records | Username: \tPassword:  | ")
    log.debug(f"1:  | ")

    wait_time = between(1, 2)
    host = 'd'
    
    @task
    def my_task(self):
        print(f"my_argument={self.environment.parsed_options.my_argument}")
        print(f"my_argument={self.environment.parsed_options.env}")
        print(f"my_ui_invisible_argument={self.environment.parsed_options.my_ui_invisible_argument}")
        self.log.debug(f"1:  | {self.user_count}")


# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(WebsiteUser)        