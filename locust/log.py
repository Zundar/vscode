from loguru import logger
from termcolor import colored

# Удаление предыдущих обработчиков
logger.remove()
# Добавление нового обработчика, который выведет цвета по умолчанию
logger.add(
    lambda msg: print(msg, end=''), 
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{module}.py:{line}</cyan> - <level>{message}</level>",
    colorize=True  # Включение цвета
)
