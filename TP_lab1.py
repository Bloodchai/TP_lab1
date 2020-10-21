import WeatherProvider
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select

engine = create_engine('sqlite:///weather.sqlite3')
metadata = MetaData()
weather = Table(
    'weather',
    metadata,
    Column('date', String),
    Column('mint', Float),
    Column('maxt', Float),
    Column('location', String),
    Column('humidity', Float),
)
metadata.create_all(engine)

c = engine.connect()

provider = WeatherProvider.WeatherProvider('9882fbe5bd364ef1885201031202010')
c.execute(weather.insert(), provider.get_data('Volgograd, Russia', '2020-09-20', '2020-09-29'))

for row in c.execute(select([weather])):
    print(row)