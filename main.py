from models import notebooks, engine, metadata
from sqlalchemy import select, func
from crud import show_top_five
from scrap_citilink import scrap_citilink
from scrap_dns import scrap_dns


# перед запуском main.py не забудьте подключить БД и задать параметры для поиска в settings.py

def show_must_go_on():
    # проверяем существуют ли данные в БД и таблица
    conn = engine.connect()
    if conn.execute(select(func.count(notebooks.c.name))).fetchone()[0] > 0:
        show_top_five()
    else:  # создаём таблицу и начинаем парсить
        print("I'm working, just wait...")
        metadata.create_all(engine)
        print("Database created. Scrap, scrap, scrap...")
        scrap_citilink()
        print("Citilink done...")
        print("Go Next victim...")
        scrap_dns()
        print("Scrap, scrap, scrap...")
        print("All done!")
        show_top_five()


if __name__ == '__main__':
    show_must_go_on()
