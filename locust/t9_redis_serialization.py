from loguru import logger
import redis
import json

from termcolor import colored

# Создаем объект Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Словарь для сохранения в Redis
q = {'r': 2, 'w': 'qwe'}
logger.warning(colored(f"==>> q: {q}", "red"))

# Сериализация словаря в строку JSON
q_json = json.dumps(q)
logger.warning(colored(f"==>> json.dumps(q): {json.dumps(q)}", "red"))

# Сохранение сериализованного словаря в Redis с ключом 'my_dict'
r.set('my_dict', q_json)

# Получение и десериализация данных из Redis
q_retrieved_json = r.get('my_dict')
logger.warning(colored(f"==>> type(q_retrieved_json): {type(q_retrieved_json)}", "blue"))
# q_retrieved_json['r'] = 'z'
logger.warning(colored(f"==>> r.get('my_dict'): {r.get('my_dict')}", "red"))
q_retrieved = json.loads(q_retrieved_json)
logger.warning(colored(f"==>> type(q_retrieved): {type(q_retrieved)}", "blue"))
q_retrieved['q'] = 'z'
q_retrieved['r'] = 'z'

print(q_retrieved)  # Вывод: {'r': 2, 'w': 'qwe'}
