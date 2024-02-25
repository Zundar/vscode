from loguru import logger
import redis
from termcolor import colored
import log  # noqa: F401

# Создаем подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Устанавливаем значение для ключа 'my_key'
r.set('my_key', 'my_value')

# Получаем значение для ключа 'my_key'
value = r.get('my_key')
print("Получаем значение для ключа 'my_key': ", value)  # Вывод: b'my_value'

# Устанавливаем TTL (время жизни) для ключа 'my_key'
logger.warning(colored(f"==>> r.ttl('my_key'): {r.ttl('my_key')}", "green"))
r.expire('my_key', 10)

# Проверяем TTL для ключа 'my_key'
ttl = r.ttl('my_key')
print("Проверяем TTL для ключа 'my_key': ", ttl)  # Вывод: 10

# Удаляем ключ 'my_key'
r.delete('my_key')

# Проверяем наличие ключа 'my_key'
exists = r.exists('my_key')
print("Проверяем наличие ключа 'my_key': ", exists)  # Вывод: False

# Добавляем элемент в список 'my_list'
r.delete('my_list')
# Добавляем элементы в список 'my_list'
r.lpush('my_list', 'item1')
r.lpush('my_list', 'item2')
r.rpush('my_list', 'item3') # Добавление элемента в конец списка

# Получаем список элементов из списка 'my_list'
list_elements = r.lrange('my_list', 0, -1)  # 0 - индекс начала, -1 - индекс конца
print("Получаем список элементов из списка 'my_list': ", list_elements)  # Вывод: [b'item3', b'item2', b'item1']

# Получаем элемент из списка 'my_list'
item = r.lpop('my_list')
print(item)  # Вывод: b'item1'
logger.warning(colored(f"==>> r.lrange('my_list', 0, -1): {r.lrange('my_list', 0, -1)}", "green"))
logger.warning(colored(f"==>> r.lindex('my_list', -1): {r.lindex('my_list', -1)}", "green"))
r.delete('my_list')


# Устанавливаем значение для хэш-ключа 'my_hash'
r.hset('my_hash', 'field1', 'value1')

# Получаем значение для хэш-ключа 'my_hash'
value = r.hget('my_hash', 'field1')
print(value)  # Вывод: b'value1'

# Удаляем хэш-ключ 'my_hash'
r.delete('my_hash')

# Выполнение транзакций
pipe = r.pipeline()
pipe.set('test_key', 'New value')
pipe.get('test_key')
logger.warning(colored(f"==>> pipe.execute(): {pipe.execute()}", "green"))
logger.warning(colored(f"==>> r.get('test_key'): {r.get('test_key')}", "green"))
# pipe.execute()  # ['OK', b'New value']

# Публикация и подписка на каналы
pubsub = r.pubsub()
pubsub.subscribe('mychannel')

r.publish('mychannel', 'Hello, Redis!')

for message in pubsub.listen():
    # Останавливаем прослушивание после получения первого сообщения
    logger.warning(colored(f"==>> message: {message}", "green"))
    break

message = next(pubsub.listen())
print(message)
