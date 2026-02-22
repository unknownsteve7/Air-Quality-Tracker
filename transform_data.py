import pandas as pd
import json
from datetime import datetime
from fetch_data import pollution_check, fetch_data

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai']

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def categorize_aqi(aqi):
    """Categorize AQI into health levels."""
    if aqi == 1:
        return "Good"
    elif aqi == 2:
        return "Fair"
    elif aqi == 3:
        return "Moderate"
    elif aqi == 4:
        return "Poor"
    elif aqi == 5:
        return "Very Poor"
    else:
        return "Unknown"

def validate_data(df):
    """
    Perform data quality checks on the combined dataframe.
    Returns True if valid, raises ValueError if issues found.
    """
    if df.empty:
        raise ValueError("Data Validation Failed: Dataframe is empty.")

    essential_cols = ['city', 'main.temp', 'main.aqi']
    for col in essential_cols:
        if col not in df.columns:
            raise ValueError(f"Data Validation Failed: Missing column {col}")
        if df[col].isnull().any():
            raise ValueError(f"Data Validation Failed: Null values found in {col}")

    if not df['main.temp'].between(-50, 60).all():
        invalid_temps = df[~df['main.temp'].between(-50, 60)]['main.temp'].tolist()
        raise ValueError(f"Data Validation Failed: Unrealistic temperatures found: {invalid_temps}")

    if not df['main.aqi'].between(1, 5).all():
        raise ValueError("Data Validation Failed: AQI score out of range (1-5)")

    return True

def combine_data():
    pollution_results = []
    weather_results = []

    for city in cities:
        pollution_results.append(json.loads(pollution_check(city)))
        weather_results.append(json.loads(fetch_data(city)))

    pollution_df = pd.json_normalize(
        pollution_results,
        record_path=['list'],
        meta=['coord'],
        errors='ignore'
    )
    pollution_df['city'] = cities

    weather_df = pd.json_normalize(weather_results)
    weather_df['city'] = cities

    combined_df = pd.merge(weather_df, pollution_df, on='city')

    for col in ['dt', 'sys.sunrise', 'sys.sunset']:
        if col in combined_df.columns:
            combined_df[col] = combined_df[col].apply(
                lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S')
            )

    temp_cols = ['main.temp', 'main.feels_like', 'main.temp_min', 'main.temp_max']
    for col in temp_cols:
        if col in combined_df.columns:
            combined_df[col] = combined_df[col].apply(kelvin_to_celsius)

    combined_df['air_quality_index'] = combined_df['main.aqi'].apply(categorize_aqi)

    return combined_df

if __name__ == "__main__":
    df = combine_data()
    df.to_csv('combined_data.csv', index=False)