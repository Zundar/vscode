import gevent
import logging
from locust import HttpUser, task, between
from locust.env import Environment
from locust.runners import LocalRunner
from locust.log import setup_logging
from locust.exception import LocustError

# Настройка логирования
setup_logging("INFO", None)
logger = logging.getLogger(__name__)

class MyHttpUser(HttpUser):
    wait_time = between(6, 7)
    host = "http://google.com"  # Установите ваш базовый URL

    @task
    def my_task(self):
        r = self.client.get("/")  # Пример запроса
        logger.warning((f"==>> r: {r}", "green"))


if __name__ == "__main__":
    # Создаем окружение с нашими пользовательскими классами
    env = Environment(user_classes=[MyHttpUser])
    runner = LocalRunner(env)

    try:
        # Ступени по нагрузке
        stages = [
            (10, 2, 10),  # (пользователи, скорость создания, время в секундах)
            (20, 5, 20),
            (30, 10, 30)
        ]

        for user_count, spawn_rate, duration in stages:
            logger.info(f"Запуск {user_count} пользователей с скоростью {spawn_rate} пользователей в секунду на {duration} секунд")
            runner.start(user_count=user_count, spawn_rate=spawn_rate)
            gevent.sleep(duration)

    except LocustError as e:
        logger.error("LocustError: %s", e)

    finally:
        # Останавливаем тесты
        runner.quit()

        # Логирование общей статистики
        stats = env.stats.total
        logger.info("Number of requests: %d", stats.num_requests)
        logger.info("Number of failures: %d", stats.num_failures)
        logger.info("Total average response time: %.2f ms", stats.avg_response_time)
        logger.info("Total median response time: %.2f ms", stats.median_response_time)
        logger.info("Total min response time: %.2f ms", stats.min_response_time)
        logger.info("Total max response time: %.2f ms", stats.max_response_time)