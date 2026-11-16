import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

model_data = joblib.load(
    "models/temperature_model.pkl"
)

model = model_data["model"]

features = model_data["features"]


# ============================================================
# 2. LOAD DATA
# ============================================================

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
# 3. CREATE TARGET
# ============================================================

# Tomorrow's temperature
df["target_temp"] = df["temp"].shift(-1)


# Remove last row because tomorrow's temperature
# is not available
df = df.dropna(
    subset=["target_temp"]
).reset_index(drop=True)


# ============================================================
# 4. REMOVE ROWS WITH MISSING FEATURES
# ============================================================

df = df.dropna(
    subset=features
).reset_index(drop=True)


# ============================================================
# 5. CREATE TRAIN / TEST DATA
# ============================================================

# We only evaluate on the unseen test period.
test = df[
    df["datetime"] >= "2025-01-01"
].copy()


X_test = test[features]

y_test = test["target_temp"]


# ============================================================
# 6. MAKE PREDICTIONS
# ============================================================

predictions = model.predict(
    X_test
)


# ============================================================
# 7. CALCULATE PERFORMANCE METRICS
# ============================================================

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


# ============================================================
# 8. PRINT MODEL PERFORMANCE
# ============================================================

print("\n")
print("=" * 55)
print("       TEMPERATURE MODEL EVALUATION")
print("=" * 55)

print(
    f"\nTest period: "
    f"{test['datetime'].min().date()} "
    f"to "
    f"{test['datetime'].max().date()}"
)

print(
    f"\nNumber of test samples: {len(test)}"
)

print("\nMODEL PERFORMANCE")
print("-" * 55)

print(
    f"MAE  : {mae:.3f} °C"
)

print(
    f"RMSE : {rmse:.3f} °C"
)

print(
    f"R²   : {r2:.3f}"
)

print("-" * 55)


# ============================================================
# 9. CREATE ACTUAL VS PREDICTED DATAFRAME
# ============================================================

results = pd.DataFrame({

    "Date": test["datetime"].dt.date,

    "Actual_Temperature":
        y_test.values,

    "Predicted_Temperature":
        predictions

})


# Calculate absolute error
results["Absolute_Error"] = abs(
    results["Actual_Temperature"]
    -
    results["Predicted_Temperature"]
)


# ============================================================
# 10. DISPLAY FIRST 20 PREDICTIONS
# ============================================================

print("\n")
print("=" * 55)
print("       ACTUAL VS PREDICTED")
print("=" * 55)

print(
    results.head(20).to_string(
        index=False
    )
)


# ============================================================
# 11. SAVE RESULTS TO CSV
# ============================================================

results.to_csv(
    "data/processed/temperature_predictions.csv",
    index=False
)

print(
    "\nPrediction results saved to:"
)

print(
    "data/processed/temperature_predictions.csv"
)


# ============================================================
# 12. ACTUAL VS PREDICTED GRAPH
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    results["Date"],
    results["Actual_Temperature"],
    label="Actual Temperature"
)

plt.plot(
    results["Date"],
    results["Predicted_Temperature"],
    label="Predicted Temperature"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Temperature (°C)"
)

plt.title(
    "Actual vs Predicted Temperature"
)

plt.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()


# Save graph
plt.savefig(
    "data/processed/actual_vs_predicted.png",
    dpi=300
)

plt.show()


# ============================================================
# 13. PREDICTION ERROR GRAPH
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    results["Date"],
    results["Absolute_Error"]
)

plt.axhline(
    y=mae,
    linestyle="--",
    label=f"MAE = {mae:.2f} °C"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Absolute Error (°C)"
)

plt.title(
    "Temperature Prediction Error"
)

plt.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()


# Save error graph
plt.savefig(
    "data/processed/prediction_error.png",
    dpi=300
)

plt.show()


# ============================================================
# 14. FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 55)
print("       EVALUATION COMPLETE")
print("=" * 55)

print(
    "\nGraphs created:"
)

print(
    "1. data/processed/actual_vs_predicted.png"
)

print(
    "2. data/processed/prediction_error.png"
)

print("\n")