import pandas as pd
import numpy as np

def generate_synthetic_weather(df):
    """
    Generates synthetic Temperature, Humidity, and Wind Speed based on seasonal and daily patterns.
    Used when external meteorological data is not available.
    """
    data = df.copy()
    
    # Ensure datetime features exist
    if 'month' not in data.columns: 
        data['month'] = data['Datetime'].dt.month
    if 'hour' not in data.columns: 
        data['hour'] = data['Datetime'].dt.hour
    
    # 1. Temperature: Annual Cycle (Peak May) + Daily Cycle (Peak 2PM)
    # 25C base - 10C swing for season + 5C swing for day + noise
    annual_temp = 25 - 10 * np.cos(2 * np.pi * (data['month'] - 1) / 12)
    daily_temp = 5 * np.cos(2 * np.pi * (data['hour'] - 14) / 24)
    data['Temperature'] = annual_temp + daily_temp + np.random.normal(0, 2, len(data))
    
    # 2. Humidity: Inverse to Temp, Higher in Monsoon (June-Sept)
    is_monsoon = (data['month'] >= 6) & (data['month'] <= 9)
    humidity_base = 50 + 20 * is_monsoon
    daily_humid = -10 * np.cos(2 * np.pi * (data['hour'] - 14) / 24)
    data['Humidity'] = humidity_base + daily_humid + np.random.normal(0, 5, len(data))
    data['Humidity'] = data['Humidity'].clip(10, 100)
    
    # 3. Wind Speed: Higher in Summer/Monsoon
    data['WindSpeed'] = 10 + 5 * np.sin(2 * np.pi * (data['month'] - 1) / 12) + np.random.normal(0, 3, len(data))
    data['WindSpeed'] = data['WindSpeed'].clip(0, 50)
    
    return data

def create_time_features(df):
    """
    Creates temporal features from Datetime column.
    """
    df = df.copy()
    df['hour'] = df['Datetime'].dt.hour
    df['month'] = df['Datetime'].dt.month
    df['day_of_week'] = df['Datetime'].dt.dayofweek
    return df
    
def add_lags_and_rolling(df, cols, lag_hours=[1, 6, 24], rolling_hours=[6, 24]):
    """
    Adds lag and rolling mean features for specified columns.
    """
    df = df.sort_values(['StationId', 'Datetime'])
    
    for col in cols:
        # Lags
        for lag in lag_hours:
            df[f'{col}_lag_{lag}'] = df.groupby('StationId')[col].shift(lag)
            
        # Rolling
        for window in rolling_hours:
            df[f'{col}_roll_{window}'] = df.groupby('StationId')[col].rolling(window=window).mean().reset_index(level=0, drop=True)
            
    return df
