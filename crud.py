from models import notebooks, engine
import re
import datetime
from sqlalchemy import select

from settings import WEIGHT_SSD, WEIGHT_RAM, WEIGTH_PRICE


# обрабатываем полученные данные с ситилинка и заносим в БД
def insert_from_citilink(price, href, title):
    name = title.split(',')[0]
    # Код, индийский код. Через регулярки собираем данные
    try:
        cpu_hhz = float(*re.findall(r'[0-9]\.[0-9]', re.findall(r'[0-9]\.[0-9]ГГц', title)[0]))
    except:
        try:
            cpu_hhz = float(*re.findall(r'[0-9]', re.findall(r'[0-9]ГГц', title)[0]))
        except:
            cpu_hhz = 1.12345
    ram_gb = int(''.join(re.findall(r'[0-9]', re.findall(r'\s\d{1,2}ГБ', title)[0].strip())))
    try:
        ssd_gb = int(''.join(re.findall(r'[0-9]', re.findall(r'\d{3,5}ГБ', title)[0])))
    except:
        try:
            ssd_gb = int(''.join(re.findall(r'[0-9]', re.findall(r'\d{1,3}ТБ', title)[0]))) * 1024
        except:
            try:
                ssd_gb = int(''.join(re.findall(r'[0-9]', re.findall(r'\d{1,3}ГБ eMMC', title)[0])))
            except:
                ssd_gb = int(''.join(re.findall(r'[0-9]', re.findall(r'\d{1,3}ГБ SSD', title)[0])))

    rank = ram_gb * WEIGHT_RAM + price * (- WEIGTH_PRICE) + ssd_gb * WEIGHT_SSD

    # заносим всё в БД
    conn = engine.connect()
    ins = notebooks.insert().values(url=href, visited_at=datetime.datetime.now(),
                                    name=name, cpu_hhz=cpu_hhz, ram_ggb=ram_gb, ssd_ggb=ssd_gb,
                                    price=price, rank=rank
                                    )
    conn.execute(ins)
    conn.close()


# обрабатываем полученные данные с DNS и заносим в БД
def insert_from_dns(price, href, title):
    name = title.split(' [')[0]
    # Код, индийский код. Через регулярки собираем данные
    try:
        cpu_hhz = float(''.join(re.findall(r'[0-9.]', re.findall(r'\s?[0-9]?.\d+\sГГц', title)[0])))
    except:
        cpu_hhz = 1.23456
    ram_gb = int(''.join(re.findall(r'\d{1,3}', re.findall(r'RAM\s\d{1,3}\sГБ', title)[0])))
    price = int(price.split('₽')[0].replace(' ', ''))

    try:
        ssd_gb = int(''.join(re.findall(r'\d{1,3}', re.findall(r'eMMC\s\d{1,4}\sГБ', title)[0])))
    except:
        try:
            ssd_gb = int(''.join(re.findall(r'\d{1,3}', re.findall(r'SSD\s\d{1,3}\sГБ', title)[0])))
        except:
            try:
                ssd_gb = int(''.join(re.findall(r'\d{1,3}', re.findall(r'HDD\s\d{1,4}\sГБ', title)[0])))
            except:
                ssd_gb = 1

    rank = ram_gb * WEIGHT_RAM + price * (- WEIGTH_PRICE) + ssd_gb * WEIGHT_SSD

    # заносим всё в БД
    conn = engine.connect()
    ins = notebooks.insert().values(url=href, visited_at=datetime.datetime.now(),
                                    name=name, cpu_hhz=cpu_hhz, ram_ggb=ram_gb, ssd_ggb=ssd_gb,
                                    price=price, rank=rank
                                    )
    conn.execute(ins)
    conn.close()


# выводим топ 5 ноутов по рейтингу из базы
def show_top_five():
    conn = engine.connect()
    s = select(notebooks.c.url, notebooks.c.name, notebooks.c.price, notebooks.c.rank).order_by(
        notebooks.c.rank.desc())
    result = conn.execute(s)
    conn.close()
    print(*result.fetchmany(5), sep='\n')
