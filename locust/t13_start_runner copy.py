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
    wait_time = between(1, 3)
    host = "http://your-testing-url.com"  # Установите ваш базовый URL

    @task
    def my_task(self):
        print("my_task")  # Пример запроса


if __name__ == "__main__":
    # Создаем окружение с нашими пользовательскими классами
    env = Environment(user_classes=[MyHttpUser])
    runner = LocalRunner(env)

    try:
        # Запуск генерации нагрузки (например, 10 пользователей с скоростью 2 новых пользователя в секунду)
        runner.start(user_count=6, spawn_rate=2)

        # Работаем 10 секунд
        gevent.sleep(10)

    except LocustError as e:
        logger.error("LocustError: %s", e)

    finally:
        # Останавливаем тесты
        runner.quit()

        # Логирование общей статистики
        logger.info("Number of requests: %d", env.stats.total.num_requests)
        logger.info("Number of failures: %d", env.stats.total.num_failures)
        logger.info("Total average response time: %d", env.stats.total.avg_response_time)