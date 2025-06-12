from app.api_client import get_station_measurements, get_station_metadata
import app.util as util

def main():
    util.load_stations_to_json()
    util.extract_station_measurements_all()
    util.load_measurements_to_db()

if __name__ == "__main__":
    main()