import pandas as pd

file_path = "data/processed/kolkata_weather_2017_2026.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET INFO ==========")
print(df.info())

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== STATISTICS ==========")
print(df.describe())