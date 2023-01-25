from sqlalchemy import create_engine, Integer, MetaData, Table, VARCHAR, Column, TIMESTAMP, Float
from settings import DATABASE_URL

# описываем нашу таблицу и создаём, если не существует
metadata = MetaData()

notebooks = Table(
    'notebooks',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('url', VARCHAR),
    Column('visited_at', TIMESTAMP),
    Column('name', VARCHAR),
    Column('cpu_hhz', Float),
    Column('ram_ggb', Integer),
    Column('ssd_ggb', Integer),
    Column('price', Integer),
    Column('rank', Float)
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
