from flask import Blueprint
import json

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/<station_id>')
def fetch_weather_station(station_id):
    with open(f"data/station_metadata.json", 'r') as file:
        stations = json.load(file)

    for station in stations:
        if station['station_id'] == station_id:
            return json.dumps(station), 200, {'Content-Type': 'application/json;'}
            
    return json.dumps({"err": 404}), 404, {'Content-Type': 'application/json;'}

@weather_bp.route('/<station_id>/<year>/<month>/<day>')
def fetch_weather_data(station_id,year,month,day):
    with open(f"data/weather/{station_id}/{year}/{month}/{day}", 'r') as file:
        data = file.read()
        return data, 200, {'Content-Type': 'text/plain; charset=utf-8'}