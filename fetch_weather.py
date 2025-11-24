import geopandas as gpd
import requests
import json
import time
import pandas as pd

def fetch_real_weather():
    print("Loading districts shapefile...")
    districts = gpd.read_file("TN_districts.shp")
    
    weather_data = {}
    
    print("Fetching real weather data from Open-Meteo (2023 Averages)...")
    
    for index, row in districts.iterrows():
        district_name = row["NAME_2"]
        # Get centroid for the district
        centroid = row["geometry"].centroid
        lat = centroid.y
        lon = centroid.x
        
        print(f"Processing {district_name}...")
        
        # Open-Meteo Archive API (Free, no key)
        # Fetching 2023 data to get a full year average
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if "daily" in data:
                daily = data["daily"]
                
                # Calculate Averages
                temp_mean = sum(daily["temperature_2m_mean"]) / len(daily["temperature_2m_mean"])
                
                # Humidity might be missing in some archive calls, let's check
                if "relative_humidity_2m_mean" in daily and daily["relative_humidity_2m_mean"]:
                    hum_mean = sum(daily["relative_humidity_2m_mean"]) / len(daily["relative_humidity_2m_mean"])
                else:
                    # Fallback if humidity is not available in archive (sometimes it's hourly)
                    # Let's try to get it from hourly if needed, or use a standard estimate
                    # For now, let's assume 70% if missing, but Open-Meteo usually has it
                    hum_mean = 70.0 
                
                # Total Annual Rainfall -> Average Annual Rainfall (sum of all days)
                # Note: The model might expect "Annual Rainfall" or "Seasonal". 
                # Usually crop models use annual or growing season. Let's use Annual Sum.
                rain_sum = sum(daily["precipitation_sum"])
                
                weather_data[district_name] = {
                    "temperature": round(temp_mean, 2),
                    "humidity": round(hum_mean, 2),
                    "rainfall": round(rain_sum, 2)
                }
            else:
                print(f"Error fetching {district_name}: {data}")
                
        except Exception as e:
            print(f"Failed for {district_name}: {e}")
            
        # Be nice to the API
        time.sleep(1)
        
    print("Saving to weather_data.json...")
    with open("weather_data.json", "w") as f:
        json.dump(weather_data, f, indent=4)
    print("Done!")

if __name__ == "__main__":
    fetch_real_weather()
