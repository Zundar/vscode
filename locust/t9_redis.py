import redis

# Подключение к Redis на локальном хосте (по умолчанию порт 6379)
# Если Redis запущен в Docker-контейнере и порт прокинут наружу, используйте 'localhost'
r = redis.Redis(host='localhost', port=6379, db=0)

# Установка значения по ключу
r.set('test_key', 'Hello, Redis!')

# Получение значения по ключу
value = r.get('test_key')
print(value)  # Выведет: b'Hello, Redis!'

# Удаление ключа
r.delete('test_key')


