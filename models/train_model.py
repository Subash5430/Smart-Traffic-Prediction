import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import joblib

data = pd.read_csv("../data/traffic_data.csv")

X = data[['latitude', 'longitude', 'hour', 'day', 'traffic_volume']]
y = data['accident']

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, 5))

model = Sequential([
    Input(shape=(1, 5)),
    LSTM(64),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])

model.fit(X_scaled, y, epochs=50, batch_size=4)

model.save("traffic_lstm.h5")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model trained & saved")
