from loguru import logger
from termcolor import colored

def func(param)->int:
    return param*2

logger.warning(colored(f"==>> func('d'): {func(7)}", "red"))