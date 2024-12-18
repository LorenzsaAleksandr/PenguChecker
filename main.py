# Импортируем модуль для генерации случайных чисел
import random

# Импортируем модуль для работы со временем
import time

# Импортируем библиотеку для обхода защиты от ботов Cloudflare
import cloudscraper

# Импортируем логгер для ведения журнала событий
from loguru import logger


# Функция для проверки кошелька на наличие airdrop
def check_wallet():
    # Бесконечный цикл для повторной попытки при возникновении ошибки
    while True:
        try:
            # Отправляем GET-запрос к API с адресом кошелька
            response = session.get(f'https://api.clusters.xyz/v0.1/airdrops/pengu/eligibility/{wallet_address}?')
            # Проверяем статус ответа
            if response.status_code == 200:
                # Преобразуем ответ в JSON формат
                data = response.json()
                # Если количество airdrop больше нуля
                if data['total'] > 0:
                    # Записываем данные о кошельке и количестве airdrop в файл
                    with open('eligible.txt', 'a+') as f:
                        f.write(f"{wallet_address}\t{data['total']}\n")
                # Возвращаем количество airdrop
                return data['total']
            else:
                # Логируем предупреждение, если статус ответа не 200
                logger.warning(f'response - {response.text}')
        # Обрабатываем любые исключения
        except Exception as e:
            # Логируем ошибку
            logger.error(e)


# Проверка, является ли этот скрипт основным исполняемым файлом
if __name__ == "__main__":
    # Создаем сессию для обхода защиты Cloudflare
    session = cloudscraper.create_scraper()

    # Открываем файл с адресами кошельков и читаем их
    wallet_addresses = open('wallets.txt', 'r').readlines()

    # Проходимся по каждому адресу кошелька
    for wallet_address in wallet_addresses:
        # Убираем лишние пробелы и символы новой строки
        wallet_address = wallet_address.strip()

        # Вызываем функцию проверки кошелька
        result = check_wallet()

        # Если результат не пустой
        if result:
            # Логируем успешную проверку
            logger.success(f'{wallet_address} {result}')
        else:
            # Логируем информацию об отсутствии airdrop
            logger.info(f'{wallet_address} not eligible')

        # Ждем случайное время от 1 до 5 секунд перед следующей проверкой
        time.sleep(random.randint(1, 5))
