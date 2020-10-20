import requests
import json
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self, location, start_date, end_date):
        url = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx'
        params = {
            'q': location,
            'date': f'{start_date}',
            'enddate': f'{end_date}',
            'tp': 24,
            'format': 'json',
            'key': self.key,
        }
        data = requests.get(url, params).json()
        with open('myWeatherData.json', 'w') as outfile:
            json.dump(data, outfile, indent = 4)
        print(data['data']["weather"][0]["maxtempC"])
        # return [
        #     {
        #         'date': row['datetimeStr'][:10],
        #         'mint': row['mint'],
        #         'maxt': row['maxt'],
        #         'location': 'Volgograd,Russia',
        #         'humidity': row['humidity'],
        #     }
        #     for row in data['locations'][location]['values']
        # ]
        return data


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

provider = WeatherProvider('9882fbe5bd364ef1885201031202010')
c.execute(weather.insert(), provider.get_data('Volgograd, Russia', '2020-09-20', '2020-09-29'))

#for row in c.execute(select([weather])):
#    print(row)