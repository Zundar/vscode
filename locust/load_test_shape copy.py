from locust import LoadTestShape

class MyLoadTestShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()

        if run_time < 10:
            # Распределение нагрузки на протяжении первой минуты
            user_count = 10
        else:
            # Распределение нагрузки после первой минуты
            user_count = 5

        return (user_count, 1)  # возвращаем кортеж (количество воркеров, продолжительность)
