from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import joblib
import requests
import pandas as pd

from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env.local"

MODEL_PATH = BASE_DIR / "models" / "temperature_model.pkl"


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True
)

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")

LOCATION = "Kolkata, India"

TIMEZONE = ZoneInfo("Asia/Kolkata")


# ============================================================
# STARTUP DEBUG
# ============================================================

print("ENV PATH:", ENV_PATH)
print("ENV EXISTS:", ENV_PATH.exists())
print("API KEY FOUND:", bool(API_KEY))

print("MODEL PATH:", MODEL_PATH)
print("MODEL EXISTS:", MODEL_PATH.exists())


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Kolkata Weather Intelligence API",
    description=(
        "Live Kolkata weather and machine-learning "
        "temperature forecasting API"
    ),
    version="5.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD ML MODEL
# ============================================================

saved_model_object = None
temperature_model = None
model_features = None
model_error = None
model_dictionary_keys = None


def load_temperature_model():

    global saved_model_object
    global temperature_model
    global model_features
    global model_error
    global model_dictionary_keys

    try:

        saved_model_object = joblib.load(
            MODEL_PATH
        )

        # ----------------------------------------------------
        # MODEL WAS SAVED AS A DICTIONARY
        # ----------------------------------------------------

        if isinstance(
            saved_model_object,
            dict
        ):

            model_dictionary_keys = list(
                saved_model_object.keys()
            )

            possible_model_keys = [
                "model",
                "best_model",
                "estimator",
                "regressor",
                "pipeline",
                "temperature_model",
            ]

            for key in possible_model_keys:

                candidate = (
                    saved_model_object.get(key)
                )

                if (
                    candidate is not None
                    and hasattr(
                        candidate,
                        "predict"
                    )
                ):

                    temperature_model = candidate
                    break


            possible_feature_keys = [
                "features",
                "feature_names",
                "feature_columns",
                "selected_features",
                "input_features",
                "columns",
            ]

            for key in possible_feature_keys:

                candidate = (
                    saved_model_object.get(key)
                )

                if candidate is not None:

                    try:

                        model_features = list(
                            candidate
                        )

                        break

                    except TypeError:
                        pass


            # Search dictionary values if the model
            # was stored using an unusual key.

            if temperature_model is None:

                for value in (
                    saved_model_object.values()
                ):

                    if hasattr(
                        value,
                        "predict"
                    ):

                        temperature_model = value
                        break


        # ----------------------------------------------------
        # MODEL SAVED DIRECTLY
        # ----------------------------------------------------

        else:

            if hasattr(
                saved_model_object,
                "predict"
            ):

                temperature_model = (
                    saved_model_object
                )


        # ----------------------------------------------------
        # GET FEATURE NAMES FROM SKLEARN MODEL
        # ----------------------------------------------------

        if (
            model_features is None
            and temperature_model is not None
            and hasattr(
                temperature_model,
                "feature_names_in_"
            )
        ):

            model_features = (
                temperature_model
                .feature_names_in_
                .tolist()
            )


        if temperature_model is None:

            model_error = (
                "Model file loaded, but no "
                "predictable estimator was found."
            )


    except Exception as error:

        model_error = str(error)


load_temperature_model()


# ============================================================
# MODEL FEATURES
# ============================================================

EXPECTED_FEATURES = [
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
    "humidity_rolling_7",
]


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message":
            "Kolkata Weather Intelligence API is running",

        "status":
            "online",

        "location":
            LOCATION,

        "api_key_found":
            bool(API_KEY),

        "temperature_model_loaded":
            temperature_model is not None,

        "backend_port":
            8080,
    }


# ============================================================
# STATUS
# ============================================================

@app.get("/status")
def status():

    now = datetime.now(
        TIMEZONE
    )

    return {
        "status":
            "online",

        "server":
            "FastAPI",

        "location":
            LOCATION,

        "date":
            now.strftime(
                "%A, %d %B %Y"
            ),

        "time":
            now.strftime(
                "%I:%M:%S %p"
            ),

        "timezone":
            "Asia/Kolkata",

        "env_file":
            str(ENV_PATH),

        "env_exists":
            ENV_PATH.exists(),

        "api_key_found":
            bool(API_KEY),

        "temperature_model_loaded":
            temperature_model is not None,
    }


# ============================================================
# MODEL INFO
# ============================================================

@app.get("/model-info")
def model_info():

    return {
        "loaded":
            temperature_model is not None,

        "saved_object_type":
            (
                type(
                    saved_model_object
                ).__name__
                if saved_model_object
                is not None
                else None
            ),

        "model_type":
            (
                type(
                    temperature_model
                ).__name__
                if temperature_model
                is not None
                else None
            ),

        "model_path":
            str(MODEL_PATH),

        "dictionary_keys":
            model_dictionary_keys,

        "features":
            (
                model_features
                if model_features
                else EXPECTED_FEATURES
            ),

        "feature_count":
            len(EXPECTED_FEATURES),

        "error":
            model_error,
    }


# ============================================================
# CHECK API KEY
# ============================================================

def ensure_api_key():

    if not API_KEY:

        raise RuntimeError(
            "Visual Crossing API key not found. "
            "Check .env.local."
        )


# ============================================================
# FETCH CURRENT WEATHER
# ============================================================

def fetch_current_weather():

    ensure_api_key()

    url = (
        "https://weather.visualcrossing.com/"
        "VisualCrossingWebServices/rest/services/"
        "timeline/"
        f"{LOCATION}"
    )

    params = {
        "unitGroup":
            "metric",

        "include":
            "current",

        "key":
            API_KEY,

        "contentType":
            "json",
    }


    response = requests.get(
        url,
        params=params,
        timeout=30
    )


    if response.status_code != 200:

        raise RuntimeError(
            "Visual Crossing current weather "
            f"request failed: {response.status_code} "
            f"{response.text}"
        )


    data = response.json()

    current = data.get(
        "currentConditions",
        {}
    )


    if not current:

        raise RuntimeError(
            "Visual Crossing returned no "
            "currentConditions."
        )


    return data, current


# ============================================================
# LIVE WEATHER
# ============================================================

@app.get("/live-weather")
def live_weather():

    try:

        data, current = (
            fetch_current_weather()
        )

        now = datetime.now(
            TIMEZONE
        )

        return {
            "location":
                LOCATION,

            "temperature":
                current.get("temp"),

            "feels_like":
                current.get("feelslike"),

            "conditions":
                current.get("conditions"),

            "humidity":
                current.get("humidity"),

            "pressure":
                current.get("pressure"),

            "visibility":
                current.get("visibility"),

            "wind_speed":
                current.get("windspeed"),

            "wind_direction":
                current.get("winddir"),

            "wind_gust":
                current.get("windgust"),

            "cloud_cover":
                current.get("cloudcover"),

            "uv_index":
                current.get("uvindex"),

            "precipitation":
                current.get("precip"),

            "precipitation_probability":
                current.get("precipprob"),

            "date":
                now.strftime(
                    "%A, %d %B %Y"
                ),

            "time":
                now.strftime(
                    "%I:%M:%S %p"
                ),

            "datetime":
                now.isoformat(),

            "observation_time":
                current.get("datetime"),

            "timezone":
                data.get(
                    "timezone",
                    "Asia/Kolkata"
                ),

            "source":
                "Visual Crossing",

            "status":
                "live",
        }


    except Exception as error:

        return {
            "error":
                str(error)
        }


# ============================================================
# FETCH RECENT DAILY WEATHER HISTORY
# ============================================================

def fetch_recent_history():

    ensure_api_key()

    today = datetime.now(
        TIMEZONE
    ).date()

    # We need a 30-day rolling feature.
    # Fetch extra days for safety.

    start_date = (
        today - timedelta(days=40)
    )

    end_date = today


    url = (
        "https://weather.visualcrossing.com/"
        "VisualCrossingWebServices/rest/services/"
        "timeline/"
        f"{LOCATION}/"
        f"{start_date.isoformat()}/"
        f"{end_date.isoformat()}"
    )


    params = {
        "unitGroup":
            "metric",

        "include":
            "days",

        "key":
            API_KEY,

        "contentType":
            "json",
    }


    response = requests.get(
        url,
        params=params,
        timeout=30
    )


    if response.status_code != 200:

        raise RuntimeError(
            "Historical weather request failed: "
            f"{response.status_code} "
            f"{response.text}"
        )


    data = response.json()

    days = data.get(
        "days",
        []
    )


    if len(days) < 30:

        raise RuntimeError(
            "Not enough historical weather data "
            f"was returned. Received {len(days)} days."
        )


    rows = []


    for day in days:

        rows.append(
            {
                "date":
                    day.get("datetime"),

                "temp":
                    day.get("temp"),

                "humidity":
                    day.get("humidity"),
            }
        )


    history = pd.DataFrame(
        rows
    )


    history["date"] = (
        pd.to_datetime(
            history["date"]
        )
    )


    history["temp"] = (
        pd.to_numeric(
            history["temp"],
            errors="coerce"
        )
    )


    history["humidity"] = (
        pd.to_numeric(
            history["humidity"],
            errors="coerce"
        )
    )


    history = (
        history
        .dropna(
            subset=[
                "temp",
                "humidity",
            ]
        )
        .sort_values("date")
        .reset_index(drop=True)
    )


    if len(history) < 30:

        raise RuntimeError(
            "Less than 30 usable historical "
            "weather rows remain after cleaning."
        )


    return history


# ============================================================
# BUILD TOMORROW MODEL INPUT
# ============================================================

def create_tomorrow_features(
    history: pd.DataFrame
):

    tomorrow = (
        datetime.now(TIMEZONE)
        + timedelta(days=1)
    )


    temperatures = (
        history["temp"]
        .astype(float)
        .tolist()
    )


    humidities = (
        history["humidity"]
        .astype(float)
        .tolist()
    )


    if len(temperatures) < 30:

        raise RuntimeError(
            "At least 30 temperature values "
            "are required."
        )


    if len(humidities) < 7:

        raise RuntimeError(
            "At least 7 humidity values "
            "are required."
        )


    # ========================================================
    # TOMORROW'S CALENDAR FEATURES
    # ========================================================

    month = tomorrow.month

    day_of_year = (
        tomorrow
        .timetuple()
        .tm_yday
    )

    day_of_week = (
        tomorrow.weekday()
    )


    # ========================================================
    # TEMPERATURE LAGS
    #
    # Tomorrow:
    # lag 1 = today's daily temperature
    # lag 2 = yesterday
    # lag 3 = 2 days ago
    # lag 7 = 6 days ago
    # ========================================================

    temp_lag_1 = temperatures[-1]

    temp_lag_2 = temperatures[-2]

    temp_lag_3 = temperatures[-3]

    temp_lag_7 = temperatures[-7]


    # ========================================================
    # HUMIDITY LAGS
    # ========================================================

    humidity_lag_1 = (
        humidities[-1]
    )

    humidity_lag_7 = (
        humidities[-7]
    )


    # ========================================================
    # ROLLING TEMPERATURE FEATURES
    #
    # These represent the data available before tomorrow,
    # therefore the latest historical value is included.
    # ========================================================

    temp_rolling_7 = float(
        pd.Series(
            temperatures[-7:]
        ).mean()
    )


    temp_rolling_30 = float(
        pd.Series(
            temperatures[-30:]
        ).mean()
    )


    humidity_rolling_7 = float(
        pd.Series(
            humidities[-7:]
        ).mean()
    )


    feature_values = {
        "month":
            month,

        "day_of_year":
            day_of_year,

        "day_of_week":
            day_of_week,

        "temp_lag_1":
            temp_lag_1,

        "temp_lag_2":
            temp_lag_2,

        "temp_lag_3":
            temp_lag_3,

        "temp_lag_7":
            temp_lag_7,

        "humidity_lag_1":
            humidity_lag_1,

        "humidity_lag_7":
            humidity_lag_7,

        "temp_rolling_7":
            temp_rolling_7,

        "temp_rolling_30":
            temp_rolling_30,

        "humidity_rolling_7":
            humidity_rolling_7,
    }


    model_input = pd.DataFrame(
        [
            [
                feature_values[
                    feature
                ]
                for feature
                in EXPECTED_FEATURES
            ]
        ],
        columns=EXPECTED_FEATURES
    )


    return (
        model_input,
        feature_values,
        tomorrow
    )


# ============================================================
# PREDICT TOMORROW
# ============================================================

@app.get("/predict-tomorrow")
def predict_tomorrow():

    if temperature_model is None:

        return {
            "error":
                "Temperature model is not loaded.",

            "details":
                model_error,
        }


    try:

        history = (
            fetch_recent_history()
        )


        (
            model_input,
            feature_values,
            tomorrow,

        ) = create_tomorrow_features(
            history
        )


        prediction = (
            temperature_model
            .predict(
                model_input
            )[0]
        )


        predicted_temperature = round(
            float(prediction),
            2
        )


        return {
            "location":
                LOCATION,

            "prediction_date":
                tomorrow.strftime(
                    "%A, %d %B %Y"
                ),

            "predicted_temperature":
                predicted_temperature,

            "unit":
                "°C",

            "model":
                type(
                    temperature_model
                ).__name__,

            "features_used":
                EXPECTED_FEATURES,

            "feature_values":
                feature_values,

            "history_days_used":
                len(history),

            "status":
                "prediction",

            "source":
                "Trained ML temperature model",
        }


    except Exception as error:

        return {
            "error":
                "Prediction failed",

            "details":
                str(error),

            "model_type":
                (
                    type(
                        temperature_model
                    ).__name__
                    if temperature_model
                    is not None
                    else None
                ),
        }