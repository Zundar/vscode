import gevent
from gevent import Greenlet
from gevent import monkey
monkey.patch_all()

import time


# Определение функции для greenlet
def my_function(name, delay):
    for i in range(5):
        print(f"{name}: {i}")
        gevent.sleep(delay)


# Создание и запуск greenlet
greenlet1 = Greenlet.spawn(my_function, "Task1", 1)
greenlet2 = Greenlet.spawn(my_function, "Task2", 0.5)

# Использование основного цикла для контроля greenlets
try:
    while True:
        print("Main Loop: Monitoring greenlets")
        # можем добавить условие завершения или контроль за их состоянием
        if not greenlet1 or not greenlet2:
            print("One of the greenlets has finished")
            break
        gevent.sleep(1)
except KeyboardInterrupt:
    print("Main Loop: Stopping greenlets on interrupt")
    greenlet1.kill()
    greenlet2.kill()

# Дождемся завершения greenlets
greenlet1.join()
greenlet2.join()

print("All greenlets have finished")