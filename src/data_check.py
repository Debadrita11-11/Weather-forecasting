import pandas as pd

# Location of our Kolkata weather dataset
file_path = r"C:\Users\gdeba\OneDrive\Desktop\weather intelligence\Data\raw\Kolkata_weather_data(2017-2022).csv"

# Load the dataset
weather_data = pd.read_csv(file_path)

print("===== FIRST 5 ROWS =====")
print(weather_data.head())

print("\n===== DATASET SIZE =====")
print(weather_data.shape)

print("\n===== COLUMN NAMES =====")
print(weather_data.columns.tolist())

print("\n===== DATA TYPES =====")
print(weather_data.dtypes)

print("\n===== MISSING VALUES =====")
print(weather_data.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(weather_data.duplicated().sum())