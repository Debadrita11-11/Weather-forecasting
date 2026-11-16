import pandas as pd
import joblib


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

model_data = joblib.load(
    "models/temperature_model.pkl"
)

model = model_data["model"]

features = model_data["features"]


# ==========================================
# 2. LOAD FEATURE DATA
# ==========================================

df = pd.read_csv(
    "data/processed/kolkata_weather_features.csv"
)

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df = df.sort_values(
    "datetime"
).reset_index(drop=True)


# ==========================================
# 3. GET LATEST WEATHER DATA
# ==========================================

latest = df.iloc[-1]

print("\n========== LATEST WEATHER DATA ==========")

print(
    "Latest date:",
    latest["datetime"].date()
)

print(
    "Latest temperature:",
    latest["temp"],
    "°C"
)


# ==========================================
# 4. CREATE INPUT DATA
# ==========================================

X = pd.DataFrame(
    [latest[features].values],
    columns=features
)


# ==========================================
# 5. MAKE PREDICTION
# ==========================================

prediction = model.predict(X)

tomorrow_temperature = prediction[0]


# ==========================================
# 6. DISPLAY RESULT
# ==========================================

print("\n==========================================")

print(
    "Predicted temperature for tomorrow:"
)

print(
    round(tomorrow_temperature, 2),
    "°C"
)

print(
    "=========================================="
)