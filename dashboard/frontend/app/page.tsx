"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";

// ============================================================
// TYPES
// ============================================================

type WeatherData = {
  location: string;

  temperature: number | null;
  feels_like: number | null;

  conditions: string | null;

  humidity: number | null;
  pressure: number | null;
  visibility: number | null;

  wind_speed: number | null;
  wind_direction: number | null;
  wind_gust: number | null;

  cloud_cover: number | null;
  uv_index: number | null;

  precipitation?: number | null;
  precipitation_probability?: number | null;

  date?: string;
  time?: string;
  datetime?: string;

  observation_time?: string | null;

  timezone?: string;

  source: string;
  status?: string;
};

type PredictionData = {
  location: string;

  prediction_date: string;

  predicted_temperature: number;

  unit: string;

  model: string;

  status: string;

  source?: string;
};

// ============================================================
// MAIN COMPONENT
// ============================================================

export default function Home() {
  // ----------------------------------------------------------
  // LIVE WEATHER STATE
  // ----------------------------------------------------------

  const [weather, setWeather] =
    useState<WeatherData | null>(null);

  const [weatherLoading, setWeatherLoading] =
    useState(true);

  const [weatherError, setWeatherError] =
    useState("");

  // ----------------------------------------------------------
  // PREDICTION STATE
  // ----------------------------------------------------------

  const [prediction, setPrediction] =
    useState<PredictionData | null>(null);

  const [predictionLoading, setPredictionLoading] =
    useState(true);

  const [predictionError, setPredictionError] =
    useState("");

  // ----------------------------------------------------------
  // LIVE CLOCK STATE
  // ----------------------------------------------------------

  const [currentTime, setCurrentTime] =
    useState<Date | null>(null);

  // ==========================================================
  // FETCH LIVE WEATHER
  // ==========================================================

  async function fetchWeather() {
    try {
      setWeatherError("");

      const response = await fetch(
        `http://127.0.0.1:8080/live-weather?_=${Date.now()}`,
        {
          method: "GET",
          cache: "no-store",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        setWeatherError(
          "Unable to load live Kolkata weather."
        );
        return;
      }

      const data = await response.json();

      if (data.error) {
        console.warn(
          "Live weather unavailable:",
          data
        );

        setWeatherError(
          data.details ||
            data.error ||
            "Unable to load live Kolkata weather."
        );

        return;
      }

      setWeather(data);
      setWeatherError("");
    } catch (error) {
      console.warn(
        "Weather server temporarily unavailable:",
        error
      );

      setWeatherError(
        "Unable to connect to the live weather server."
      );
    } finally {
      setWeatherLoading(false);
    }
  }

  // ==========================================================
  // FETCH TOMORROW PREDICTION
  // ==========================================================

  async function fetchPrediction() {
    try {
      setPredictionError("");

      const response = await fetch(
        `http://127.0.0.1:8080/predict-tomorrow?_=${Date.now()}`,
        {
          method: "GET",
          cache: "no-store",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        setPredictionError(
          "Tomorrow's prediction is currently unavailable."
        );
        return;
      }

      const data = await response.json();

      if (data.error) {
        console.warn(
          "Prediction unavailable:",
          data
        );

        setPredictionError(
          data.details ||
            data.error ||
            "Tomorrow's prediction is currently unavailable."
        );

        return;
      }

      setPrediction(data);
      setPredictionError("");
    } catch (error) {
      console.warn(
        "Prediction server temporarily unavailable:",
        error
      );

      setPredictionError(
        "Tomorrow's prediction is currently unavailable."
      );
    } finally {
      setPredictionLoading(false);
    }
  }

  // ==========================================================
  // INITIAL FETCH + AUTOMATIC REFRESH
  // ==========================================================

  useEffect(() => {
    fetchWeather();
    fetchPrediction();

    const refreshInterval = setInterval(() => {
      fetchWeather();
      fetchPrediction();
    }, 5 * 60 * 1000);

    return () => {
      clearInterval(refreshInterval);
    };
  }, []);

  // ==========================================================
  // LIVE KOLKATA CLOCK
  // ==========================================================

  useEffect(() => {
    setCurrentTime(new Date());

    const clockInterval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => {
      clearInterval(clockInterval);
    };
  }, []);

  // ==========================================================
  // KOLKATA DATE
  // ==========================================================

  const kolkataDate = currentTime
    ? new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        weekday: "long",
        day: "2-digit",
        month: "long",
        year: "numeric",
      }).format(currentTime)
    : "--";

  // ==========================================================
  // KOLKATA TIME
  // ==========================================================

  const kolkataTime = currentTime
    ? new Intl.DateTimeFormat("en-IN", {
        timeZone: "Asia/Kolkata",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      }).format(currentTime)
    : "--";

  // ==========================================================
  // PAGE
  // ==========================================================

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl">

        {/* HEADER */}
        <motion.header
          initial={{
            opacity: 0,
            y: -20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.6,
          }}
          className="mb-10"
        >
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
            Weather Intelligence
          </p>

          <h1 className="mt-3 text-4xl font-bold md:text-6xl">
            Kolkata Weather
          </h1>

          <p className="mt-3 text-slate-400">
            Live weather monitoring and machine-learning temperature forecasting
          </p>
        </motion.header>

        {/* LIVE KOLKATA DATE + CLOCK */}
        <motion.section
          initial={{
            opacity: 0,
            y: 15,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.6,
          }}
          className="mb-6 rounded-3xl border border-slate-800 bg-slate-900 p-6"
        >
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div>
              <p className="text-sm uppercase tracking-widest text-cyan-400">
                Kolkata Local Date
              </p>

              <p className="mt-2 text-xl font-semibold">
                {kolkataDate}
              </p>
            </div>

            <div className="text-left md:text-right">
              <p className="text-4xl font-bold tracking-tight">
                {kolkataTime}
              </p>

              <p className="mt-1 text-sm text-slate-500">
                Asia/Kolkata
              </p>
            </div>
          </div>
        </motion.section>

        {/* LIVE WEATHER LOADING */}
        {weatherLoading && (
          <div className="rounded-3xl border border-slate-800 bg-slate-900 p-10 text-center">
            <p className="text-lg text-slate-300">
              Loading live Kolkata weather...
            </p>
          </div>
        )}

        {/* WEATHER ERROR */}
        {weatherError && !weatherLoading && (
          <div className="rounded-3xl border border-red-900 bg-red-950/40 p-8">
            <h2 className="text-xl font-semibold text-red-400">
              Weather Connection Error
            </h2>

            <p className="mt-2 text-slate-300">
              {weatherError}
            </p>

            <button
              onClick={fetchWeather}
              className="mt-5 rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-slate-200"
            >
              Try Again
            </button>
          </div>
        )}

        {/* CURRENT WEATHER */}
        {weather && !weatherLoading && (
          <>
            <motion.section
              initial={{
                opacity: 0,
                y: 20,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              transition={{
                duration: 0.7,
              }}
              className="rounded-3xl border border-slate-800 bg-slate-900 p-8 shadow-2xl"
            >
              <div className="flex flex-col justify-between gap-8 md:flex-row">

                {/* LEFT */}
                <div>
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 animate-pulse rounded-full bg-emerald-400" />

                    <p className="text-sm uppercase tracking-widest text-emerald-400">
                      Live Weather
                    </p>
                  </div>

                  <h2 className="mt-3 text-2xl font-semibold">
                    {weather.location}
                  </h2>

                  <p className="mt-2 text-lg text-slate-300">
                    {weather.conditions ||
                      "Conditions unavailable"}
                  </p>

                  <p className="mt-4 text-sm text-slate-500">
                    Weather source: {weather.source}
                  </p>
                </div>

                {/* TEMPERATURE */}
                <div className="text-left md:text-right">
                  <p className="text-7xl font-bold tracking-tight">
                    {weather.temperature !== null &&
                    weather.temperature !== undefined
                      ? `${weather.temperature.toFixed(1)}°C`
                      : "--"}
                  </p>

                  <p className="mt-2 text-slate-400">
                    Current Temperature
                  </p>
                </div>
              </div>

              {/* DATE / TIME / OBSERVATION */}
              <div className="mt-8 grid gap-4 border-t border-slate-800 pt-6 md:grid-cols-3">
                <InfoBlock
                  title="Today's Date"
                  value={kolkataDate}
                />

                <InfoBlock
                  title="Current Time"
                  value={kolkataTime}
                />

                <InfoBlock
                  title="Weather Observation"
                  value={
                    weather.observation_time || "--"
                  }
                />
              </div>
            </motion.section>

            {/* WEATHER DETAILS */}
            <section className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
              <WeatherCard
                title="Feels Like"
                value={
                  weather.feels_like !== null &&
                  weather.feels_like !== undefined
                    ? `${weather.feels_like.toFixed(1)}°C`
                    : "--"
                }
              />

              <WeatherCard
                title="Humidity"
                value={
                  weather.humidity !== null &&
                  weather.humidity !== undefined
                    ? `${weather.humidity.toFixed(0)}%`
                    : "--"
                }
              />

              <WeatherCard
                title="Wind Speed"
                value={
                  weather.wind_speed !== null &&
                  weather.wind_speed !== undefined
                    ? `${weather.wind_speed.toFixed(1)} km/h`
                    : "--"
                }
              />

              <WeatherCard
                title="Pressure"
                value={
                  weather.pressure !== null &&
                  weather.pressure !== undefined
                    ? `${weather.pressure.toFixed(1)} hPa`
                    : "--"
                }
              />

              <WeatherCard
                title="Visibility"
                value={
                  weather.visibility !== null &&
                  weather.visibility !== undefined
                    ? `${weather.visibility.toFixed(1)} km`
                    : "--"
                }
              />

              <WeatherCard
                title="Cloud Cover"
                value={
                  weather.cloud_cover !== null &&
                  weather.cloud_cover !== undefined
                    ? `${weather.cloud_cover.toFixed(0)}%`
                    : "--"
                }
              />

              <WeatherCard
                title="UV Index"
                value={
                  weather.uv_index !== null &&
                  weather.uv_index !== undefined
                    ? `${weather.uv_index.toFixed(1)}`
                    : "--"
                }
              />

              <WeatherCard
                title="Wind Gust"
                value={
                  weather.wind_gust !== null &&
                  weather.wind_gust !== undefined
                    ? `${weather.wind_gust.toFixed(1)} km/h`
                    : "--"
                }
              />
            </section>
          </>
        )}

        {/* TOMORROW ML PREDICTION */}
        <motion.section
          initial={{
            opacity: 0,
            y: 20,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.8,
          }}
          className="mt-6 rounded-3xl border border-cyan-900 bg-cyan-950/30 p-8"
        >
          <p className="text-sm uppercase tracking-widest text-cyan-400">
            Machine Learning Forecast
          </p>

          <h2 className="mt-2 text-2xl font-semibold">
            Tomorrow&apos;s Temperature Prediction
          </h2>

          {predictionLoading ? (
            <p className="mt-6 text-slate-400">
              Calculating prediction...
            </p>
          ) : prediction ? (
            <>
              <div className="mt-6 flex items-end gap-3">
                <span className="text-6xl font-bold">
                  {prediction.predicted_temperature.toFixed(1)}
                </span>

                <span className="pb-2 text-xl text-slate-400">
                  °C
                </span>
              </div>

              <p className="mt-5 text-slate-300">
                Forecast for {prediction.prediction_date}
              </p>

              <div className="mt-5 grid gap-4 md:grid-cols-2">
                <InfoBlock
                  title="Machine Learning Model"
                  value={prediction.model}
                />

                <InfoBlock
                  title="Prediction Status"
                  value="ML Forecast"
                />
              </div>

              <p className="mt-5 text-sm text-slate-500">
                This prediction is generated by your trained machine-learning
                model using recent Kolkata weather history.
              </p>
            </>
          ) : (
            <>
              <p className="mt-6 text-red-400">
                {predictionError ||
                  "Prediction unavailable."}
              </p>

              <button
                onClick={fetchPrediction}
                className="mt-5 rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300"
              >
                Retry Prediction
              </button>
            </>
          )}
        </motion.section>

        {/* FOOTER */}
        <footer className="mt-8 grid gap-2 text-sm text-slate-500 md:grid-cols-3">
          <p>
            Weather: Visual Crossing
          </p>

          <p className="md:text-center">
            Data refresh: every 5 minutes
          </p>

          <p className="md:text-right">
            Clock refresh: every second
          </p>
        </footer>
      </div>
    </main>
  );
}

// ============================================================
// WEATHER CARD
// ============================================================

function WeatherCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <motion.div
      whileHover={{
        y: -4,
      }}
      className="rounded-2xl border border-slate-800 bg-slate-900 p-5"
    >
      <p className="text-sm text-slate-500">
        {title}
      </p>

      <p className="mt-2 text-xl font-semibold">
        {value}
      </p>
    </motion.div>
  );
}

// ============================================================
// INFO BLOCK
// ============================================================

function InfoBlock({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div>
      <p className="text-xs uppercase tracking-widest text-slate-500">
        {title}
      </p>

      <p className="mt-1 font-medium text-slate-200">
        {value}
      </p>
    </div>
  );
}