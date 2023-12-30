# В файле load_test_shape.py

from locust import LoadTestShape

class MyLoadTestShape(LoadTestShape):
    user_count = 10
    spawn_rate = 1

# изменим способ передачи параметров в LoadTestShape. Вместо передачи параметров через конструктор, 
# воспользуемся атрибутами класса для хранения параметров и методом класса для их установки.
# Теперь параметры хранятся в атрибутах класса MyLoadTestShape, и метод set_params позволяет устанавливать их из скрипта
    @classmethod
    def set_params(cls, type, user_count, spawn_rate):
        cls.type = type
        cls.user_count = user_count
        cls.spawn_rate = spawn_rate

    def tick(self):
        run_time = self.get_run_time()
        print(f'{self.type}')

        if self.type == 'stab':
            return (3, 1)
        else:
            if run_time < 10:
                user_count = self.user_count
                spawn_rate = self.spawn_rate
            else:
                user_count = self.user_count // 2
                spawn_rate = self.spawn_rate // 2

            return (user_count, spawn_rate)
