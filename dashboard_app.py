import streamlit as st
import pandas as pd
import pickle
from fetch_data import fetch_weather_data, fetch_holiday_data
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Load pre-trained model
with open("demand_forecast_model.pkl", "rb") as f:
    model = pickle.load(f)

# Function to fetch weather and holiday data
def fetch_data():
    # Fetch weather data (you can modify this to match your data source)
    weather_df = fetch_weather_data()

    # Fetch holidays (you can modify this to match your data source)
    try:
        holidays = fetch_holiday_data()
    except Exception as e:
        holidays = []

    # Add 'hour' column
    weather_df['hour'] = pd.to_datetime(weather_df['datetime']).dt.hour

    # Add 'holiday' column (1 for holiday, 0 for non-holiday)
    weather_df['holiday'] = 0  # Default 0
    if holidays:
        for date in holidays:
            weather_df.loc[weather_df['datetime'].str.startswith(date), 'holiday'] = 1

    return weather_df

# Function to predict demand
def predict_demand(weather_df, model):
    # Select features for prediction
    X = weather_df[['temperature', 'humidity', 'wind_speed', 'holiday', 'hour']]
    
    # Predict demand
    weather_df['predicted_demand'] = model.predict(X)
    
    return weather_df

# Streamlit dashboard
st.title("Electricity Demand Forecast Dashboard ⚡")

# Date Range Selector for Prediction
start_date = st.date_input('Start Date', min_value=datetime.date.today())
end_date = st.date_input('End Date', min_value=start_date)

# Fetch data and make predictions
weather_df = fetch_data()
weather_df = predict_demand(weather_df, model)

# Filter the weather data by the selected date range
weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
filtered_df = weather_df[(weather_df['datetime'].dt.date >= start_date) & (weather_df['datetime'].dt.date <= end_date)]

# Display filtered data
st.write(f"### Weather and Demand Prediction Data ({start_date} to {end_date})")
st.dataframe(filtered_df)

# Plot Temperature vs Predicted Demand
st.write("### Temperature vs Predicted Demand")
st.line_chart(filtered_df.set_index('datetime')[['predicted_demand', 'temperature']])

# Plot Power Demand over Time (Area chart)
st.write("### Predicted Demand Over Time")
st.area_chart(filtered_df.set_index('datetime')['predicted_demand'])

# Additional Insights (e.g., Impact of Holidays)
holiday_impact_df = filtered_df.groupby('holiday')['predicted_demand'].mean()
st.write("### Average Predicted Demand Based on Holidays")
st.bar_chart(holiday_impact_df)

# Allow user to adjust weather parameters and see the effect on predictions
st.sidebar.header('Adjust Weather Parameters')

temp_input = st.sidebar.slider('Temperature (°C)', -10, 40, 25)
humidity_input = st.sidebar.slider('Humidity (%)', 0, 100, 50)
wind_speed_input = st.sidebar.slider('Wind Speed (km/h)', 0, 50, 15)
hour_input = st.sidebar.slider('Hour of the Day', 0, 23, 12)

# Predict demand based on user input
user_input = np.array([[temp_input, humidity_input, wind_speed_input, 0, hour_input]])  # Assuming no holiday
predicted_demand_user = model.predict(user_input)

st.sidebar.write(f"### Predicted Demand at {hour_input}:00 hrs")
st.sidebar.write(f"Predicted Demand: {predicted_demand_user[0]} MW")

# Success message
st.success("Prediction and visualization completed successfully! ✅")
