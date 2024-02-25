import random
from loguru import logger
from redis import Redis
from termcolor import colored

class FileGenerator:
    def __init__(self, filename, num_lines, min_val, max_val):
        self.filename = filename
        self.num_lines = num_lines
        self.min_val = min_val
        self.max_val = max_val

    def create_file(self):
        with open(self.filename, 'w') as f:
            for _ in range(self.num_lines):
                f.write(str(random.randint(self.min_val, self.max_val)) + '\n')

class RedisHandler:
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, db=0)
        # self.filename = filename

    def store_in_redis(self, filename):
        with open(filename, 'r') as f:
            # Чтобы сохранить данные в хеш, используем имя файла как ключ хеша
            for idx, line in enumerate(f, start=1):
                self.redis.hset(filename, f'line:{idx}', line.strip())

    def random_read(self, filename):
        # Получаем все ключи из хеша
        keys = self.redis.hkeys(filename)
        # print("HKEYS: Получить ключи хеша: ", [f.decode('utf-8') for f in keys])

        if len(keys)>0:
            random_key = random.choice(keys)
            # Читаем случайное значение из хеша
            return self.redis.hget(filename, random_key).decode('utf-8')
        else:
            return None

if __name__ == "__main__":
    file_creator = FileGenerator('random_numbers.txt', 1000, 1000000, 9000000)
    file_creator.create_file()

    r = RedisHandler()
    r.store_in_redis('random_numbers.txt')

    for i in range(10):
        print(r.random_read('random_numbers.txt'))

    r = Redis(host='localhost', port=6379, db=0)
    r.delete('random_numbers.txt')
