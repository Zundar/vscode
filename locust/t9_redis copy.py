import random
from redis import Redis
from termcolor import colored
from loguru import logger

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
    def __init__(self, filename):
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.filename = filename

    def store_in_redis(self):
        with open(self.filename, 'r') as f:
            for idx, line in enumerate(f, start=1):
                self.redis.set(f'line:{idx}', line.strip())

    def random_read(self):
        keys = self.redis.keys('line:*')
        # logger.warning(colored(f"==>> keys: {keys}", "red"))
        random_key = random.choice(keys)
        return self.redis.get(random_key).decode('utf-8')

if __name__ == "__main__":
    file_creator = FileGenerator('random_numbers.txt', 1000, 1000000, 9000000)
    file_creator.create_file()

    redis_handler = RedisHandler('random_numbers.txt')
    redis_handler.store_in_redis()

    for i in range(10):
        print(redis_handler.random_read())
