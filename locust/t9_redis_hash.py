from loguru import logger
import redis
from termcolor import colored
import log  # noqa: F401

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# HSET: Установить значение в хеш
r.delete('myhash')
r.hset('myhash', 'field1', 'value1')

# HGET: Извлечь значение из хеша
value = r.hget('myhash', 'field1')
print("HGET: Извлечь значение из хеша: ", value.decode('utf-8'))

# HSET: Установить несколько полей в хеш (используется в версиях Redis >= 4.0.0)
r.hset('myhash', mapping={'r': 2, 'w': 'qwe'})
logger.warning(colored(f"==>> int(r.hget('myhash', 'r')): {int(r.hget('myhash', 'r'))}", "green"))

name = 'key'
q = {'r': 2, 'w': 'qwe1', name: 'val'}
r.hset(name='myhash2', mapping=q)
logger.warning(colored(f"==>> r.hgetall('myhash2'): {r.hgetall('myhash2')}", "green"))
logger.warning(colored(f"==>> r.hget('myhash2', name): {r.hget('myhash2', name).decode('utf-8')}", "green"))
logger.warning(colored(f"==>> type(r.hget('myhash2', name)): {type(r.hget('myhash2', name))}", "blue"))
logger.warning(colored(f"==>> type(r.hget('myhash2', name).decode('utf-8')): {type(r.hget('myhash2', name).decode('utf-8'))}", "blue"))

r.hset('myhash', mapping={'field2': 'value2', 'field3': 'value3'})
logger.warning(colored(f"==>> r.hgetall('myhash'): {r.hgetall('myhash')}", "green"))

# HGETALL: Получить все поля и значения хеша
hash_fields_values = r.hgetall('myhash')
print("HGETALL: Получить все поля и значения хеша: ", {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_fields_values.items()})

# HDEL: Удалить поле из хеша
r.hdel('myhash', 'field1')

# HKEYS: Получить ключи хеша
fields = r.hkeys('myhash')
print("HKEYS: Получить ключи хеша: ", [f.decode('utf-8') for f in fields])

# HVALS: Получить значения хеша
values = r.hvals('myhash')
print("HVALS: Получить значения хеша: ", [v.decode('utf-8') for v in values])

# HEXISTS: Проверить наличие ключа в хеше
exists = r.hexists('myhash', 'field2')
print("HEXISTS: Проверить наличие ключа в хеше: ", 'Exists' if exists else 'Does not exist')
