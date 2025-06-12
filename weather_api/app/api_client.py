import requests
from app.config import Config

def get_station_metadata(station_id):
    url = f"{Config.BASE_URL}/{station_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response)
    
def get_station_measurements(station_id,year,month,day):
    year = str(year)
    month = str(month).zfill(2)
    day = str(day).zfill(2)

    url = f"{Config.BASE_URL}/{station_id}/{year}/{month}/{day}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(response)