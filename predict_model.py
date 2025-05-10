from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

def train_model(processed_df):
    features = ['temperature', 'humidity', 'wind_speed', 'hour', 'dayofweek', 'is_weekend', 'is_holiday']
    X = processed_df[features]
    y = processed_df['demand']  # assume we have historic demand data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    with open("demand_forecast_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    df = pd.read_csv("processed_historic_data.csv")
    train_model(df)
