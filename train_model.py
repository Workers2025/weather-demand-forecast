# train_model.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Dummy training dataset (you can replace this with real data)
X = np.random.rand(100, 5)  # 100 samples, 5 features
y = np.random.rand(100)     # 100 targets

# Train model
model = LinearRegression()
model.fit(X, y)

# Save trained model to 'demand_forecast_model.pkl'
with open("demand_forecast_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as demand_forecast_model.pkl")
