"""
***

RestUser has been removed, because the base FastHttpUser from locust-core now provides the same functionality
This file is for testing only.

***
"""

from contextlib import contextmanager
import time
from locust import task, run_single_user, FastHttpUser, SequentialTaskSet
from locust.contrib.fasthttp import RestResponseContextManager
from locust.user.wait_time import constant
from typing import Generator
from locust import events
from locust.exception import StopUser
import gevent
# from locust import events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, MasterRunner, LocalRunner
from termcolor import colored

def checker(environment, *args, **kwargs):
    print(colored(f"==>> args: {args}", "green"))
    print(colored(f"==>> _kwargs: {kwargs}", "green"))
    while not environment.runner.state in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        # time.sleep(1)
        gevent.sleep(1)
        print(f"checker: {environment.runner.stats.total.fail_ratio}")
        print(colored(f"==>> environment.runner.stats: {dir(environment.runner.stats)}", "green"))
        print(colored(f"==>> environment.runner.stats.num_failures: {(environment.runner.stats.num_failures)}", "green"))
        print(colored(f"==>> environment.runner.stats.entries: {dir(environment.runner.stats.entries)}", "green"))
        print(colored(f"==>> environment.runner.stats.entries: {list(environment.runner.stats.entries)}", "green"))
        # print(colored(f"==>> environment.runner.stats.log_request: {environment.runner.stats.log_request()}", "green"))
        print(colored(f"==>> environment.runner.stats.num_requests: {environment.runner.stats.num_requests}", "green"))
        print(colored(f"==>> environment.runner.stats.total: {environment.runner.stats.total}", "green"))

        for request in environment.runner.stats.entries:
            print(request)

        if environment.runner.stats.total.fail_ratio > 1.2:
        # if environment.runner.stats.total.fail_ratio > 0.2:
            print(f"fail ratio was {environment.runner.stats.total.fail_ratio}, quitting")
            environment.runner.quit()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    # dont run this on workers, we only care about the aggregated numbers
    if isinstance(environment.runner, MasterRunner) or isinstance(environment.runner, LocalRunner):
        print(colored(f"==>> isinstance(environment.runner: {type(environment.runner)}", "green"))
        gevent.spawn(checker, environment, 228, jj="1")


class MySequentialTaskSet(SequentialTaskSet):
    @task
    def t4(self):
        # should work
        print('4')
        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            if resp.js["data"]["foo"] == 1:
            # if resp.js["data"]["foo"] != 1:
                resp.failure(f"Unexpected value of foo in response {resp.text}")
                raise StopUser()

            # assertions are a nice short way of expressiont your expectations about the response. The AssertionError thrown will be caught
            # and fail the request, including the message and the payload in the failure content
            # assert resp.js["data"]["foo"] != 1, "Unexpected value of foo in response"

class MyUser(FastHttpUser):
    host = "https://postman-echo.com"
    wait_time = constant(180)  # be nice to postman-echo.com, and dont run this at scale.

    @task
    def t(self):
        # should work
        with self.rest("GET", "/get", json={"foo": 1}) as resp:
            if resp.js["args"]["foo"] != 1:
                resp.failure(f"Unexpected value of foo in response {resp.text}")

        # should work
        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            if resp.js["data"]["foo"] != 1:
                resp.failure(f"Unexpected value of foo in response {resp.text}")
            # assertions are a nice short way of expressiont your expectations about the response. The AssertionError thrown will be caught
            # and fail the request, including the message and the payload in the failure content
            assert resp.js["data"]["foo"] == 1, "Unexpected value of foo in response"

        # assertions are a nice short way to validate the response. The AssertionError they raise
        # will be caught by rest() and mark the request as failed

        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            # mark the request as failed with the message "Assertion failed"
            assert resp.js["data"]["foo"] == 2

        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            # custom failure message
            assert resp.js["data"]["foo"] == 2, "my custom error message"

        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            # use a trailing comma to append the response text to the custom message
            assert resp.js["data"]["foo"] == 2, "my custom error message with response text,"

        # this only works in python 3.8 and up, so it is commented out:
        # if sys.version_info >= (3, 8):
        #     with self.rest("", "/post", json={"foo": 1}) as resp:
        #         # assign and assert in one line
        #         assert (foo := resp.js["foo"])
        #         print(f"the number {foo} is awesome")

        # rest() catches most exceptions, so any programming mistakes you make automatically marks the request as a failure
        # and stores the callstack in the failure message
        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            1 / 0  # pylint: disable=pointless-statement

        # response isnt even json, but RestUser will already have been marked it as a failure, so we dont have to do it again
        with self.rest("GET", "/") as resp:
            pass

        with self.rest("GET", "/") as resp:
            # If resp.js is None (which it will be when there is a connection failure, a non-json responses etc),
            # reading from resp.js will raise a TypeError (instead of an AssertionError), so lets avoid that:
            if resp.js:
                assert resp.js["foo"] == 2
            # or, as a mildly confusing oneliner:
            assert not resp.js or resp.js["foo"] == 2

        # 404
        with self.rest("GET", "http://example.com/") as resp:
            pass

        # connection closed
        with self.rest("POST", "http://example.com:42/", json={"foo": 1}) as resp:
            pass


# An example of how you might write a common base class for an API that always requires
# certain headers, or where you always want to check the response in a certain way
class RestUserThatLooksAtErrors(FastHttpUser):
    abstract = True

    @contextmanager
    def rest(self, method, url, **kwargs) -> Generator[RestResponseContextManager, None, None]:
        extra_headers = {"my_header": "my_value"}
        with super().rest(method, url, headers=extra_headers, **kwargs) as resp:
            resp: RestResponseContextManager
            if resp.js and "error" in resp.js and resp.js["error"] is not None:
                resp.failure(resp.js["error"])
            yield resp


class MyOtherRestUser(FastHttpUser):
# class MyOtherRestUser(RestUserThatLooksAtErrors):
    host = "https://postman-echo.com"
    wait_time = constant(3)  # be nice to postman-echo.com, and dont run this at scale.
    tasks = [MySequentialTaskSet]

    @task
    def t(self):
        with self.rest("GET", "/") as _resp:
            print('1')
            pass

    @task
    def t2(self):
        # should work
        print('2')
        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            if resp.js["data"]["foo"] != 1:
                resp.failure(f"Unexpected value of foo in response {resp.text}")
            # assertions are a nice short way of expressiont your expectations about the response. The AssertionError thrown will be caught
            # and fail the request, including the message and the payload in the failure content
            assert resp.js["data"]["foo"] == 1, "Unexpected value of foo in response"
            print("🚀 ~ file: t6 event.py:137 ~ resp.js:", resp.js)

    @task
    def t3(self):
        # should work
        print('3')
        with self.rest("POST", "/post", json={"foo": 1}) as resp:
            if resp.js["data"]["foo"] == 1:
            # if resp.js["data"]["foo"] != 1:
                resp.failure(f"Unexpected value of foo in response {resp.text}")
                raise StopUser()

            # assertions are a nice short way of expressiont your expectations about the response. The AssertionError thrown will be caught
            # and fail the request, including the message and the payload in the failure content
            # assert resp.js["data"]["foo"] != 1, "Unexpected value of foo in response"

@events.request.add_listener
def on_request(request_type, name, response, response_time, response_length, exception, context, **kwargs):
    """
    Event handler that get triggered on every request.
    """
    # stats["content-length"] += response_length
    print(f'name: {name}')
    print(f'request_type: {request_type}')
    print(f'context: {context}')
    # print(f'response: {response}')
    print(f'response_time: {response_time}')
    print(f'exception: {exception}')

if __name__ == "__main__":
    run_single_user(MyUser)
