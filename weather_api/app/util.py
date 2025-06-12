import io
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from app.api_client import get_station_metadata, get_station_measurements
from datetime import datetime
import time

def get_data_year(station, year):
    station_id = station
    year = year
    
    # Check if CSV file already exists
    csv_filename = f"{station_id}_daily_avg_temp_{year}.csv"
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
    for month in range(1, 13):
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
                print(f"Processing {year}-{month:02d}-{day:02d}...")
                
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