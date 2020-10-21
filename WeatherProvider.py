import json
import requests

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
        return [
            {
                'date': row['date'][:10],
                'mint': row['mintempC'],
                'maxt': row['maxtempC'],
                'location': 'Volgograd,Russia',
                'humidity': row['hourly'][0]['humidity']
            }
            for row in data['data']['weather']
        ]
