import random
import gevent
from gevent import Greenlet
from locust import HttpUser, task, between, events, runners
from locust.env import Environment
from locust.log import setup_logging
from loguru import logger
from termcolor import colored

class MyUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://example.com"  # Установите ваш базовый URL

    @task
    def my_task(self):
        r = self.client.get("/")
        logger.warning(colored(f"==>> r: {r}", "green"))

# Определение функции для дополнительной задачи
def my_additional_task(name, delay):
    for i in range(5):
        logger.info(colored(f"{name}: {i}", "blue"))
        gevent.sleep(delay)

def init_listener(environment, **kwargs):
    logger.warning(colored(f"==>> on_locust_init called", "yellow"))

    # Создаем и запускаем greenlet для дополнительной задачи
    greenlet1 = Greenlet.spawn(my_additional_task, "AdditionalTask1", 1)
    greenlet2 = Greenlet.spawn(my_additional_task, "AdditionalTask2", 0.5)
    logger.warning(colored(f"==>> greenlet1 and greenlet2 started", "green"))

    def monitor_greenlets():
        try:
            while True:
                if environment.runner.state in [runners.STATE_STOPPING, runners.STATE_STOPPED, runners.STATE_CLEANUP]:
                    logger.info("Locust is stopping, stopping greenlets")
                    break

                logger.info("Main loop: Monitoring greenlets")
                if not greenlet1 or not greenlet2:
                    logger.info("One of the greenlets has finished")
                    break
                gevent.sleep(1)
        except KeyboardInterrupt:
            logger.info("Main loop: Stopping greenlets on interrupt")
            greenlet1.kill()
            greenlet2.kill()

        greenlet1.join()
        greenlet2.join()

        logger.info("All greenlets have finished")

    # Запуск мониторинга в отдельном greenlet
    monitor_greenlet = Greenlet.spawn(monitor_greenlets)
    monitor_greenlet.start()

if __name__ == "__main__":
    from locust.stats import stats_printer, stats_history
    from locust.log import setup_logging

    # Настройка логирования
    setup_logging("INFO", None)
    logger.warning(colored(f"==>> Starting Locust script", "yellow"))

    # Создание среды исполнения Locust
    env = Environment(user_classes=[MyUser])

    # Регистрация события init
    events.init.add_listener(init_listener)

    # Регистрация обработчиков событий тестов
    @env.events.test_start.add_listener
    def on_test_start(**kw):
        logger.info(colored("Test started", "white"))

    @env.events.test_stop.add_listener
    def on_test_stop(**kw):
        logger.info(colored("Test stopped", "white"))

    # Ручной вызов события init
    events.init.fire(environment=env)

    # Инициализация Runner'а
    logger.warning(colored(f"==>> Creating local runner", "yellow"))
    env.create_local_runner()

    # Добавление функции печати статистики и истории
    # gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    # Начало теста
    env.runner.start(1, spawn_rate=1)

    # Продолжительность теста в секундах
    gevent.spawn_later(10, lambda: env.runner.quit())

    # Ожидание завершения
    env.runner.greenlet.join()