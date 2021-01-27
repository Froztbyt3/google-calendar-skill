import requests
import json
from google_calendar import getLocationData


def weatherClient():
    location = getLocationData()
    key = 'xxxxx'

    if location == '':
        pass
    else:
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location, key))
        # TODO: remove after development
        # print('Status:', response.status_code)
        data = response.json()
        # print(data['main'].get('temp'))

        return data['main'].get('temp')


# if __name__ == '__main__':
#     weatherClient()
