from loguru import logger
import requests
from bs4 import BeautifulSoup
from termcolor import colored
import log  # noqa: F401

# URL страницы с нужной информацией
main_url = 'https://docs.rsshub.app/guide/instances'

# Функция для получения списка сайтов с основной страницы
def get_sites(main_url):
    try:
        response = requests.get(main_url, timeout=5)  # Устанавливаем таймаут 5 секунд
    except requests.Timeout:
        logger.error(f"Request to {main_url} timed out.")
        return []  # Возвращаем пустой список в случае таймаута
    except requests.RequestException as e:
        logger.error(f"Request to {main_url} failed: {e}")
        return []

    if response.status_code != 200:
        raise Exception(f"Failed to load page {main_url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Поиск таблиц с сайтами
    tables = soup.find_all('table')
    sites = []

    for table in tables:
        for row in table.find_all('tr')[1:]:  # Пропускаем заголовок таблицы
            columns = row.find_all('td')
            if columns:
                site_url = columns[0].find('a').get('href')
                logger.warning(colored(f"==>> site_url: {site_url}", "green"))
                sites.append(site_url)
    
    return sites

# Функция для посещения каждой страницы и вывода ответа
def visit_sites(sites):
    for site in sites:
        full_url = site + '/twitter/user/msvetov'
        try:
            response = requests.get(full_url, timeout=5)  # Устанавливаем таймаут 5 секунд
            logger.warning(f"Response from {full_url}:")  # Убираем детали для более четкого формата
            process_response(response)
        except requests.Timeout:
            logger.warning(f"Request to {full_url} timed out.\n\n")
        except requests.RequestException as e:
            logger.warning(f"Failed to access {full_url}: {e}\n\n")

# Функция для обработки ответа и вывода нужного содержимого
def process_response(response):
    error_message_start = response.text.find('Error Message:')
    
    if error_message_start != -1 or response.text.find('Error message:') != -1:
        # Извлекаем содержимое от 'Error Message:' до конца html блока, чтобы получить всю ошибку
        error_message = response.text[error_message_start:]
        
        # Используем BeautifulSoup для извлечения чистого текста ошибки
        soup = BeautifulSoup(error_message, "html.parser")
        error_message_text = soup.get_text(separator="\n").strip()
        
        logger.warning(colored(f"Error message found:\n{error_message_text[:100]}", "red"))
    else:
        logger.warning(colored(f"Full response:\n{response.text}", "green"))

# Получаем список сайтов и посещаем каждый из них
if __name__ == '__main__':
    sites = get_sites(main_url)
    if sites:
        visit_sites(sites)