import pandas as pd

# -----------------------------------------
# 1. Load cleaned dataset
# -----------------------------------------

input_file = "data/processed/kolkata_weather_cleaned.csv"

df = pd.read_csv(input_file)

# Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Sort chronologically
df = df.sort_values("datetime").reset_index(drop=True)


# -----------------------------------------
# 2. Create calendar features
# -----------------------------------------

df["year"] = df["datetime"].dt.year
df["month"] = df["datetime"].dt.month
df["day"] = df["datetime"].dt.day
df["day_of_year"] = df["datetime"].dt.dayofyear
df["day_of_week"] = df["datetime"].dt.dayofweek


# -----------------------------------------
# 3. Create temperature lag features
# -----------------------------------------

df["temp_lag_1"] = df["temp"].shift(1)
df["temp_lag_2"] = df["temp"].shift(2)
df["temp_lag_3"] = df["temp"].shift(3)
df["temp_lag_7"] = df["temp"].shift(7)


# -----------------------------------------
# 4. Create humidity lag features
# -----------------------------------------

df["humidity_lag_1"] = df["humidity"].shift(1)
df["humidity_lag_7"] = df["humidity"].shift(7)


# -----------------------------------------
# 5. Create rolling averages
# -----------------------------------------

df["temp_rolling_7"] = df["temp"].rolling(7).mean()
df["temp_rolling_30"] = df["temp"].rolling(30).mean()

df["humidity_rolling_7"] = df["humidity"].rolling(7).mean()


# -----------------------------------------
# 6. Remove rows created by lag/rolling
# -----------------------------------------

df = df.dropna().reset_index(drop=True)


# -----------------------------------------
# 7. Save feature dataset
# -----------------------------------------

output_file = "data/processed/kolkata_weather_features.csv"

df.to_csv(output_file, index=False)


# -----------------------------------------
# 8. Display results
# -----------------------------------------

print("FEATURE ENGINEERING COMPLETED")

print("Dataset shape:", df.shape)

print("\nFeatures:")
print(df.columns.tolist())

print("\nSaved to:")
print(output_file)