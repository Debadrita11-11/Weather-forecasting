import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. LOAD FEATURE DATA
# ==========================================

file_path = "data/processed/kolkata_weather_features.csv"

df = pd.read_csv(file_path)

df["datetime"] = pd.to_datetime(df["datetime"])

df = df.sort_values("datetime").reset_index(drop=True)


# ==========================================
# 2. CREATE TOMORROW'S TEMPERATURE TARGET
# ==========================================

df["target_temp"] = df["temp"].shift(-1)

# Remove final row because tomorrow's temperature
# is not available
df = df.dropna(subset=["target_temp"]).reset_index(drop=True)


# ==========================================
# 3. CHECK TARGET
# ==========================================

print("\n========== TARGET CHECK ==========")

print(
    df[["datetime", "temp", "target_temp"]].head(10)
)


# ==========================================
# 4. DEFINE FORECASTING FEATURES
# ==========================================

features = [

    "month",
    "day_of_year",
    "day_of_week",

    "temp_lag_1",
    "temp_lag_2",
    "temp_lag_3",
    "temp_lag_7",

    "humidity_lag_1",
    "humidity_lag_7",

    "temp_rolling_7",
    "temp_rolling_30",

    "humidity_rolling_7"
]


target = "target_temp"


# ==========================================
# 5. TIME-BASED TRAIN / TEST SPLIT
# ==========================================

train = df[df["datetime"] < "2025-01-01"]

test = df[df["datetime"] >= "2025-01-01"]


X_train = train[features]

y_train = train[target]

X_test = test[features]

y_test = test[target]


print("\n========== DATA SPLIT ==========")

print("Training data:", X_train.shape)

print("Testing data:", X_test.shape)

print("\nTraining period:")

print(
    train["datetime"].min(),
    "to",
    train["datetime"].max()
)

print("\nTesting period:")

print(
    test["datetime"].min(),
    "to",
    test["datetime"].max()
)


# ==========================================
# 6. CREATE MODELS
# ==========================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=300,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )
}


# ==========================================
# 7. TRAIN AND EVALUATE
# ==========================================

results = {}

best_model = None

best_rmse = float("inf")

best_name = None


for name, model in models.items():

    print("\n================================")

    print("Training:", name)

    print("================================")


    # Train
    model.fit(
        X_train,
        y_train
    )


    # Predict
    predictions = model.predict(
        X_test
    )


    # Metrics
    mae = mean_absolute_error(
        y_test,
        predictions
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )


    r2 = r2_score(
        y_test,
        predictions
    )


    # Store results
    results[name] = {

        "MAE": mae,

        "RMSE": rmse,

        "R2": r2
    }


    print(
        "MAE :",
        round(mae, 3)
    )

    print(
        "RMSE:",
        round(rmse, 3)
    )

    print(
        "R²  :",
        round(r2, 3)
    )


    # Select best model
    if rmse < best_rmse:

        best_rmse = rmse

        best_model = model

        best_name = name


# ==========================================
# 8. MODEL COMPARISON
# ==========================================

print(
    "\n\n========== MODEL COMPARISON =========="
)


for name, metrics in results.items():

    print(
        f"{name}: "
        f"MAE={metrics['MAE']:.3f}, "
        f"RMSE={metrics['RMSE']:.3f}, "
        f"R²={metrics['R2']:.3f}"
    )


print(
    "\n========================================"
)

print(
    "BEST MODEL:",
    best_name
)

print(
    "BEST RMSE:",
    round(best_rmse, 3)
)

print(
    "========================================"
)


# ==========================================
# 9. SAVE BEST MODEL
# ==========================================

model_data = {

    "model": best_model,

    "features": features
}


joblib.dump(

    model_data,

    "models/temperature_model.pkl"
)


print(
    "\nModel saved successfully:"
)

print(
    "models/temperature_model.pkl"
)