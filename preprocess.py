import pandas as pd

def preprocess_weather(weather_df):
    weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
    weather_df['hour'] = weather_df['datetime'].dt.hour
    weather_df['dayofweek'] = weather_df['datetime'].dt.dayofweek
    weather_df['is_weekend'] = weather_df['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)
    return weather_df

def merge_with_holidays(weather_df, holidays):
    weather_df['is_holiday'] = weather_df['datetime'].dt.date.astype(str).isin(holidays).astype(int)
    return weather_df
