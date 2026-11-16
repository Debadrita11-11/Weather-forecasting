import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Kolkata Weather Intelligence",
    page_icon="🌦️",
    layout="wide"
)


# ============================================================
# LOAD MODEL
# ============================================================

model_data = joblib.load(
    "models/temperature_model.pkl"
)

model = model_data["model"]

features = model_data["features"]


# ============================================================
# LOAD WEATHER DATA
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
# CREATE TOMORROW'S PREDICTION
# ============================================================

latest = df.iloc[-1]

X = pd.DataFrame(
    [latest[features].values],
    columns=features
)

prediction = model.predict(X)

predicted_temperature = prediction[0]


# ============================================================
# TITLE
# ============================================================

st.title("🌦️ Kolkata Weather Intelligence")

st.subheader(
    "Machine Learning Based Temperature Forecast"
)

st.markdown("---")


# ============================================================
# TOP INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Latest Temperature",
        f"{latest['temp']:.1f} °C"
    )


with col2:

    st.metric(
        "Tomorrow's Prediction",
        f"{predicted_temperature:.1f} °C"
    )


with col3:

    st.metric(
        "Model R² Score",
        "0.874"
    )


# ============================================================
# FORECAST SECTION
# ============================================================

st.markdown("---")

st.header("🌡️ Tomorrow's Temperature Forecast")

st.success(
    f"Predicted Temperature: "
    f"{predicted_temperature:.2f} °C"
)

st.info(
    "The model has an average historical "
    "prediction error of approximately ±1.11 °C."
)


# ============================================================
# HISTORICAL TEMPERATURE
# ============================================================

st.markdown("---")

st.header("📈 Historical Temperature")

fig, ax = plt.subplots(
    figsize=(14, 5)
)

ax.plot(
    df["datetime"],
    df["temp"]
)

ax.set_xlabel("Date")

ax.set_ylabel("Temperature (°C)")

ax.set_title(
    "Kolkata Temperature History"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)


# ============================================================
# ACTUAL VS PREDICTED
# ============================================================

st.markdown("---")

st.header("🤖 Actual vs Predicted Temperature")


# Load evaluation results

results = pd.read_csv(
    "data/processed/temperature_predictions.csv"
)

results["Date"] = pd.to_datetime(
    results["Date"]
)


fig2, ax2 = plt.subplots(
    figsize=(14, 5)
)

ax2.plot(
    results["Date"],
    results["Actual_Temperature"],
    label="Actual"
)

ax2.plot(
    results["Date"],
    results["Predicted_Temperature"],
    label="Predicted"
)

ax2.set_xlabel("Date")

ax2.set_ylabel("Temperature (°C)")

ax2.set_title(
    "Actual vs Predicted Temperature"
)

ax2.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig2)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown("---")

st.header("📊 Model Performance")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "MAE",
        "1.114 °C"
    )


with col2:

    st.metric(
        "RMSE",
        "1.465 °C"
    )


with col3:

    st.metric(
        "R²",
        "0.874"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Kolkata Weather Intelligence | "
    "Machine Learning Temperature Forecasting"
)