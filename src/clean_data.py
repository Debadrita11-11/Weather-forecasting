import pandas as pd

# -----------------------------------------
# 1. Load master dataset
# -----------------------------------------

input_file = "data/processed/kolkata_weather_2017_2026.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)


# -----------------------------------------
# 2. Convert datetime column
# -----------------------------------------

df["datetime"] = pd.to_datetime(df["datetime"])

# Sort by date
df = df.sort_values("datetime").reset_index(drop=True)


# -----------------------------------------
# 3. Remove unnecessary columns
# -----------------------------------------

# windgust has around 60% missing values
# snowdepth is not useful for Kolkata forecasting

df = df.drop(columns=["windgust", "snowdepth"])


# -----------------------------------------
# 4. Handle missing values
# -----------------------------------------

# Numerical columns
numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns

for column in numeric_columns:
    df[column] = df[column].interpolate(method="linear")
    df[column] = df[column].fillna(df[column].median())


# Categorical columns
df["conditions"] = df["conditions"].fillna(
    df["conditions"].mode()[0]
)


# -----------------------------------------
# 5. Remove duplicate dates
# -----------------------------------------

duplicates = df["datetime"].duplicated().sum()

print("Duplicate dates found:", duplicates)

df = df.drop_duplicates(
    subset=["datetime"],
    keep="first"
)


# -----------------------------------------
# 6. Check missing values
# -----------------------------------------

print("\nMissing values after cleaning:")
print(df.isnull().sum())


# -----------------------------------------
# 7. Save cleaned dataset
# -----------------------------------------

output_file = "data/processed/kolkata_weather_cleaned.csv"

df.to_csv(output_file, index=False)


# -----------------------------------------
# 8. Final information
# -----------------------------------------

print("\nCLEANING COMPLETED")

print("Final dataset shape:", df.shape)

print("Start date:", df["datetime"].min())

print("End date:", df["datetime"].max())

print("\nColumns:")
print(df.columns.tolist())

print("\nSaved to:")
print(output_file)