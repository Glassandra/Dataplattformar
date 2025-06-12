import io
import os
import pandas as pd
from app.api_client import get_station_metadata, get_station_measurements
from datetime import datetime
from tqdm import tqdm
from app.config import Config
import sqlite3
import json

def get_data_year(station, year):
    station_id = station
    year = year

    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Check if CSV file already exists
    csv_filename = os.path.join(data_dir, f"{station_id}_daily_avg_temp_{year}.csv")
    if os.path.exists(csv_filename):
        print(f"Loading existing data from {csv_filename}")
        results_df = pd.read_csv(csv_filename)
        # Convert date column back to datetime
        results_df['date'] = pd.to_datetime(results_df['date'])
        return results_df
    
    # If file doesn't exist, fetch data from API
    dates = []
    avg_temperatures = []
    avg_precipitation = []

    print(f"Fetching data for station {station_id} for {year}...")

    # Loop through each month
    for month in tqdm(range(1, 13)):
        # Determine days in month
        if month in [4, 6, 9, 11]:
            days_in_month = 30
        elif month == 2:
            days_in_month = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
        else:
            days_in_month = 31
        
        # Loop through each day
        for day in range(1, days_in_month + 1):
            try:
                #print(f"Processing {year}-{month:02d}-{day:02d}...")
                
                # Get data for current day
                data = get_station_measurements(station_id, year, month, day)
                
                # Parse the data
                df_day = pd.read_csv(io.StringIO(data), sep='\t', header=None, 
                                    names=['time', 'temperature', 'precipitation'])
                
                # Calculate average temperature for the day
                avg_temp = df_day['temperature'].mean()
                avg_prec = df_day['precipitation'].mean()
                
                # Store date and temperature
                date = datetime(year, month, day)
                dates.append(date)
                avg_temperatures.append(avg_temp)
                avg_precipitation.append(avg_prec)
                
            except Exception as e:
                print(f"Error for {year}-{month:02d}-{day:02d}: {str(e)}")
            
            # Short delay to avoid overwhelming the API
            #time.sleep(0.2)

    results_df = pd.DataFrame({
        'date': dates,
        'avg_temperature': avg_temperatures,
        'avg_precipitation': avg_precipitation
    })

    # Save results to CSV for future use
    results_df.to_csv(csv_filename, index=False)
    return results_df

def load_stations_to_json():
    data = extract_station_data()
    with open("data/stations.json", "w", encoding="utf-8") as f:
        data_json = json.dumps(data)
        f.write(data_json)
    print(f"Stations printed to json")

def extract_station_data():
    stations = []
    for station_id in Config.STATION_IDS:
        station_data = get_station_metadata(station_id)
        stations.append(station_data)
    return stations

def extract_station_measurements(station_id):
    dates = pd.date_range("2024-01-02", "2024-12-31", freq="D")

    first_day_data = get_station_measurements(station_id, "2024", "01", "01")
    df = pd.read_csv(io.StringIO(first_day_data), sep='\t', header=None, 
                     names=['time', 'temperature', 'precipitation'])    
    df['station_id'] = station_id

    for d in tqdm(dates):
        month_str = str(d.month).zfill(2)
        day_str = str(d.day).zfill(2)
        
        try:
            day_data = get_station_measurements(station_id, d.year, month_str, day_str)
            
            df_day = pd.read_csv(io.StringIO(day_data), sep='\t', header=None, 
                                names=['time', 'temperature', 'precipitation'])
            df_day['station_id'] = station_id
            df = pd.concat([df, df_day])
        except Exception as e:
            print(f"Error getting data for {d.year}-{month_str}-{day_str}: {str(e)}")
            continue

    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    df.to_csv(f"data/measurements_{station_id}.csv", index=False)
    return df

def extract_station_measurements_all():
    for station_id in Config.STATION_IDS:
        extract_station_measurements(station_id)

def load_measurements_to_db():
    conn = sqlite3.connect(Config.DB_CONNECTION)
    conn.execute("DROP TABLE IF EXISTS measurements")

    for station_id in Config.STATION_IDS:
        print(f"Loading {station_id} to SQL")
        df = pd.read_csv(f"data/measurements_{station_id}.csv")
        df.to_sql("measurements", conn, if_exists="append")

    conn.commit()
    conn.close()

    print("All stations loaded to SQL")
