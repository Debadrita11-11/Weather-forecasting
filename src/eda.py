import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# 1. Load cleaned Kolkata weather data
# -----------------------------------------

file_path = "Data/processed/kolkata_weather_cleaned.csv"

weather_data = pd.read_csv(file_path)

# Convert Date time to datetime
weather_data["Date time"] = pd.to_datetime(
    weather_data["Date time"]
)

print("Dataset loaded successfully!")
print("Shape:", weather_data.shape)


# -----------------------------------------
# 2. Temperature over time
# -----------------------------------------

plt.figure(figsize=(15, 6))

plt.plot(
    weather_data["Date time"],
    weather_data["Temperature"]
)

plt.title("Kolkata Temperature Over Time")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

plt.tight_layout()
plt.show()
# -----------------------------------------
# 3. Average temperature by month
# -----------------------------------------

weather_data["Month"] = weather_data["Date time"].dt.month

monthly_temperature = (
    weather_data
    .groupby("Month")["Temperature"]
    .mean()
)

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_temperature.index,
    monthly_temperature.values,
    marker="o"
)

plt.title("Average Kolkata Temperature by Month")
plt.xlabel("Month")
plt.ylabel("Average Temperature (°C)")

plt.xticks(range(1, 13))

plt.tight_layout()
plt.show()
# -----------------------------------------
# 4. Monthly rainfall
# -----------------------------------------

monthly_rainfall = (
    weather_data
    .groupby("Month")["Precipitation"]
    .sum()
)

plt.figure(figsize=(10, 6))

plt.bar(
    monthly_rainfall.index,
    monthly_rainfall.values
)

plt.title("Monthly Rainfall in Kolkata")
plt.xlabel("Month")
plt.ylabel("Total Precipitation")

plt.xticks(range(1, 13))

plt.tight_layout()
plt.show()
# -----------------------------------------
# 5. Temperature vs Relative Humidity
# -----------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    weather_data["Temperature"],
    weather_data["Relative Humidity"],
    alpha=0.5
)

plt.title("Temperature vs Relative Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Relative Humidity (%)")

plt.tight_layout()
plt.show()