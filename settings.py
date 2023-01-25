# подключаемся к БД и создаём таблицу с ноутбуками
USER = 'postgres'
PASSWORD = 'postgres'
HOST = '127.0.0.1'
NAME = 'postgres'
DATABASE_URL = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/{NAME}'

# количество страниц, которые будут собирать наши парсеры
TOTAL_PAGE_CITILINK = 10
TOTAL_PAGE_DNS = 5

# веса для подсчёта ранка
WEIGHT_RAM = 5.6
WEIGTH_PRICE = 0.0005
WEIGHT_SSD = 3

# задержка паука для страниц
TIME_SLEEP_CITILINK = 3
TIME_SLEEP_DNS = 3