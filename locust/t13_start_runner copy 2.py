import gevent
import logging
from locust import HttpUser, task, between
from locust.env import Environment
from locust.runners import LocalRunner
from locust.log import setup_logging
from locust.exception import LocustError
from termcolor import colored

# Настройка логирования
setup_logging("INFO", None)
logger = logging.getLogger(__name__)

# Классы Locust пользователей
class MyHttpUser(HttpUser):
    wait_time = between(6, 7)
    host = "http://google.com"  # Установите ваш базовый URL

    @task
    def my_task(self):
        if self.environment.runner:
            current_users = self.environment.runner.user_count
            logger.warning(f"==>> MyHttpUser: {current_users} users currently active")
        r = self.client.get("/")  # Пример запроса
        logger.warning(f"==>> MyHttpUser r: {r.status_code}")

class AnotherHttpUser(HttpUser):
    wait_time = between(3, 4)
    host = "http://example.com"  # Установите ваш базовый URL

    @task
    def another_task(self):
        if self.environment.runner:
            current_users = self.environment.runner.user_count
            logger.info(f"==>> AnotherHttpUser: {current_users} users currently active")
        r = self.client.get("/")  # Пример запроса
        logger.info(f"==>> another_task r: {r.status_code}")

# Логирование статистики
def log_stats(env, interval=5):
    while True:
        stats = env.stats.total
        logger.info("Number of requests: %d", stats.num_requests)
        logger.info("Number of failures: %d", stats.num_failures)
        logger.info("Total average response time: %.2f ms", stats.avg_response_time)
        logger.info("Total median response time: %.2f ms", stats.median_response_time)
        
        gevent.sleep(interval)

# Функция для запуска ступени нагрузки
def run_stage(env, user_class, user_count, spawn_rate, duration):
    try:
        # Проверка на существующий runner
        if env.runner is None:
            runner = env.create_local_runner()
        else:
            runner = env.runner

        logger.info(f"Запуск {user_count} пользователей с скоростью {spawn_rate} пользователей в секунду на {duration} секунд")
        runner.start(user_count=user_count, spawn_rate=spawn_rate)

        # Запуск логирования статистики
        # gevent.spawn(log_stats, env)
        
        gevent.sleep(duration)
        runner.quit()
        
        # Логирование общей статистики
        stats = env.stats.total
        logger.info("Number of requests: %d", stats.num_requests)
        logger.info("Number of failures: %d", stats.num_failures)
        logger.info("Total average response time: %.2f ms", stats.avg_response_time)
        logger.info("Total median response time: %.2f ms", stats.median_response_time)
        
        min_response_time = stats.min_response_time if stats.min_response_time is not None else 0
        max_response_time = stats.max_response_time if stats.max_response_time is not None else 0
        
        logger.info("Total min response time: %.2f ms", min_response_time)
        logger.info("Total max response time: %.2f ms", max_response_time)
    except LocustError as e:
        logger.error("LocustError: %s", e)

if __name__ == "__main__":
    # Создаем окружение для Locust
    env = Environment(user_classes=[MyHttpUser, AnotherHttpUser])

    # Определяем различные ступени нагрузки для двух классов
    stages_dict = {
        MyHttpUser: [
            (2, 4, 10),  # (пользователи, скорость создания, время в секундах)
            (3, 4, 20),
            (4, 4, 30)
        ],
        AnotherHttpUser: [
            (1, 1, 7),
            (2, 2, 15),
            (3, 3, 25)
        ]
    }

    # Запускаем ступени нагрузки последовательно
    for user_class, stages in stages_dict.items():
        for user_count, spawn_rate, duration in stages:
            run_stage(env, user_class, user_count, spawn_rate, duration)

    logger.info("Все ступени нагрузки завершены.")