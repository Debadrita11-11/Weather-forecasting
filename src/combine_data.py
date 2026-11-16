import pandas as pd
import os

# ============================================
# 1. LOAD THE THREE DATASETS
# ============================================

old_data = pd.read_csv(
    "Data/raw/kolkata_weather_data(2017-2022).csv"
)

new_data_1 = pd.read_csv(
    "Data/raw/kolkata_weather_2023_2025.csv"
)

new_data_2 = pd.read_csv(
    "Data/raw/kolkata_weather_2025_2026.csv"
)


# ============================================
# 2. RENAME OLD DATASET COLUMNS
# ============================================

old_data = old_data.rename(columns={
    "Date time": "datetime",
    "Minimum Temperature": "tempmin",
    "Maximum Temperature": "tempmax",
    "Temperature": "temp",
    "Dew Point": "dew",
    "Relative Humidity": "humidity",
    "Heat Index": "heatindex",
    "Wind Speed": "windspeed",
    "Wind Gust": "windgust",
    "Wind Direction": "winddir",
    "Wind Chill": "windchill",
    "Precipitation": "precip",
    "Precipitation Cover": "precipcover",
    "Snow Depth": "snowdepth",
    "Visibility": "visibility",
    "Cloud Cover": "cloudcover",
    "Sea Level Pressure": "sealevelpressure",
    "Weather Type": "weathertype",
    "Conditions": "conditions"
})


# ============================================
# 3. KEEP THE IMPORTANT WEATHER VARIABLES
# ============================================

columns_to_keep = [
    "datetime",
    "tempmin",
    "tempmax",
    "temp",
    "dew",
    "humidity",
    "windspeed",
    "windgust",
    "winddir",
    "precip",
    "precipcover",
    "snowdepth",
    "visibility",
    "cloudcover",
    "sealevelpressure",
    "conditions"
]


# ============================================
# 4. KEEP ONLY COMMON COLUMNS
# ============================================

old_data = old_data[
    [col for col in columns_to_keep if col in old_data.columns]
]

new_data_1 = new_data_1[
    [col for col in columns_to_keep if col in new_data_1.columns]
]

new_data_2 = new_data_2[
    [col for col in columns_to_keep if col in new_data_2.columns]
]


# ============================================
# 5. CONVERT DATE COLUMN
# ============================================

old_data["datetime"] = pd.to_datetime(
    old_data["datetime"],
    errors="coerce"
)

new_data_1["datetime"] = pd.to_datetime(
    new_data_1["datetime"],
    errors="coerce"
)

new_data_2["datetime"] = pd.to_datetime(
    new_data_2["datetime"],
    errors="coerce"
)


# ============================================
# 6. COMBINE THE THREE DATASETS
# ============================================

combined_data = pd.concat(
    [
        old_data,
        new_data_1,
        new_data_2
    ],
    ignore_index=True
)


# ============================================
# 7. SORT BY DATE
# ============================================

combined_data = combined_data.sort_values(
    by="datetime"
)


# ============================================
# 8. CHECK DUPLICATE DATES
# ============================================

duplicate_dates = combined_data["datetime"].duplicated().sum()

print("\nDuplicate dates before removal:")
print(duplicate_dates)


# ============================================
# 9. REMOVE DUPLICATE DATES
# ============================================

combined_data = combined_data.drop_duplicates(
    subset=["datetime"],
    keep="first"
)


# ============================================
# 10. RESET INDEX
# ============================================

combined_data = combined_data.reset_index(drop=True)


# ============================================
# 11. CREATE PROCESSED FOLDER
# ============================================

os.makedirs(
    "Data/processed",
    exist_ok=True
)


# ============================================
# 12. SAVE MASTER DATASET
# ============================================

output_file = (
    "Data/processed/"
    "kolkata_weather_2017_2026.csv"
)

combined_data.to_csv(
    output_file,
    index=False
)


# ============================================
# 13. FINAL CHECK
# ============================================

print("\n===================================")
print("MASTER DATASET CREATED")
print("===================================")

print(
    "\nDataset shape:",
    combined_data.shape
)

print(
    "\nStart date:",
    combined_data["datetime"].min()
)

print(
    "End date:",
    combined_data["datetime"].max()
)

print(
    "\nNumber of days:",
    len(combined_data)
)

print("\nMissing values:")
print(combined_data.isnull().sum())

print("\nSaved to:")
print(output_file)