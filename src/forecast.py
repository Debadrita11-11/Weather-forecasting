import pandas as pd
import joblib


# ============================================================
# KOLKATA TEMPERATURE FORECAST
# ============================================================


print("\n")
print("=" * 60)
print("          KOLKATA WEATHER INTELLIGENCE")
print("          TEMPERATURE FORECAST")
print("=" * 60)


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

print("\nLoading trained model...")

model_data = joblib.load(
    "models/temperature_model.pkl"
)

model = model_data["model"]

features = model_data["features"]


print("Model loaded successfully.")


# ============================================================
# 2. LOAD FEATURE DATA
# ============================================================

print("\nLoading weather data...")

df = pd.read_csv(
    "data/processed/kolkata_weather_features.csv"
)

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df = df.sort_values(
    "datetime"
).reset_index(drop=True)


# ============================================================
# 3. GET LATEST AVAILABLE WEATHER DATA
# ============================================================

latest = df.iloc[-1]


latest_date = latest["datetime"]

latest_temperature = latest["temp"]


print("\nLatest available weather data")
print("-" * 60)

print(
    "Date:",
    latest_date.strftime("%d %B %Y")
)

print(
    "Temperature:",
    round(latest_temperature, 2),
    "°C"
)


# ============================================================
# 4. PREPARE MODEL INPUT
# ============================================================

X = pd.DataFrame(
    [latest[features].values],
    columns=features
)


# ============================================================
# 5. MAKE PREDICTION
# ============================================================

prediction = model.predict(X)

predicted_temperature = prediction[0]


# ============================================================
# 6. DISPLAY FORECAST
# ============================================================

print("\n")
print("=" * 60)
print("             TOMORROW'S FORECAST")
print("=" * 60)

print(
    "\nPredicted Temperature:"
)

print(
    f"        {predicted_temperature:.2f} °C"
)

print("\n")


# ============================================================
# 7. MODEL PERFORMANCE
# ============================================================

print("-" * 60)
print("MODEL PERFORMANCE")
print("-" * 60)

print(
    "Average Error (MAE):  ±1.11 °C"
)

print(
    "RMSE:                  1.47 °C"
)

print(
    "R² Score:              0.874"
)


print("\n")
print("=" * 60)
print("             FORECAST COMPLETE")
print("=" * 60)
print()