"use client";

import { useEffect, useState } from "react";
import { motion } from "motion/react";

type WeatherData = {
  location: string;
  datetime: string;
  temperature: number | null;
  feels_like: number | null;
  humidity: number | null;
  windspeed: number | null;
  windgust: number | null;
  conditions: string | null;
  cloudcover: number | null;
  visibility: number | null;
  pressure: number | null;
  source: string;
};

export default function Home() {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchWeather() {
    try {
      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/live-weather",
        {
          cache: "no-store",
        }
      );

      if (!response.ok) {
        throw new Error("Unable to fetch live weather");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setWeather(data);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the weather server.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchWeather();

    // Refresh weather every 10 minutes
    const interval = setInterval(fetchWeather, 10 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="mx-auto max-w-6xl">

        {/* HEADER */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-10"
        >
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
            Weather Intelligence
          </p>

          <h1 className="mt-3 text-4xl font-bold md:text-6xl">
            Kolkata Weather
          </h1>

          <p className="mt-3 text-slate-400">
            Live weather monitoring and machine-learning prediction
          </p>
        </motion.div>

        {/* LOADING */}
        {loading && (
          <div className="rounded-3xl border border-slate-800 bg-slate-900 p-10 text-center">
            <p className="text-lg text-slate-300">
              Loading live weather...
            </p>
          </div>
        )}

        {/* ERROR */}
        {error && !loading && (
          <div className="rounded-3xl border border-red-900 bg-red-950/40 p-8">
            <h2 className="text-xl font-semibold text-red-400">
              Connection Error
            </h2>

            <p className="mt-2 text-slate-300">
              {error}
            </p>

            <button
              onClick={fetchWeather}
              className="mt-5 rounded-xl bg-white px-5 py-3 font-semibold text-black transition hover:bg-slate-200"
            >
              Try Again
            </button>
          </div>
        )}

        {/* WEATHER */}
        {weather && !loading && (
          <>
            {/* CURRENT WEATHER */}
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
              className="rounded-3xl border border-slate-800 bg-slate-900 p-8 shadow-2xl"
            >
              <div className="flex flex-col justify-between gap-8 md:flex-row">

                <div>
                  <p className="text-sm uppercase tracking-widest text-cyan-400">
                    Live Now
                  </p>

                  <h2 className="mt-2 text-2xl font-semibold">
                    {weather.location}
                  </h2>

                  <p className="mt-2 text-slate-400">
                    {weather.conditions}
                  </p>
                </div>

                <div className="text-left md:text-right">
                  <p className="text-7xl font-bold tracking-tight">
                    {weather.temperature !== null
                      ? `${weather.temperature.toFixed(1)}°`
                      : "--"}
                  </p>

                  <p className="mt-2 text-slate-400">
                    Current temperature
                  </p>
                </div>
              </div>
            </motion.section>

            {/* DETAILS */}
            <section className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">

              <WeatherCard
                title="Feels Like"
                value={
                  weather.feels_like !== null
                    ? `${weather.feels_like.toFixed(1)}°C`
                    : "--"
                }
              />

              <WeatherCard
                title="Humidity"
                value={
                  weather.humidity !== null
                    ? `${weather.humidity.toFixed(0)}%`
                    : "--"
                }
              />

              <WeatherCard
                title="Wind Speed"
                value={
                  weather.windspeed !== null
                    ? `${weather.windspeed.toFixed(1)} km/h`
                    : "--"
                }
              />

              <WeatherCard
                title="Pressure"
                value={
                  weather.pressure !== null
                    ? `${weather.pressure.toFixed(1)} hPa`
                    : "--"
                }
              />

            </section>

            {/* PREDICTION */}
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mt-6 rounded-3xl border border-cyan-900 bg-cyan-950/30 p-8"
            >
              <p className="text-sm uppercase tracking-widest text-cyan-400">
                Machine Learning
              </p>

              <h2 className="mt-2 text-2xl font-semibold">
                Tomorrow's Temperature Prediction
              </h2>

              <div className="mt-6 flex items-end gap-3">
                <span className="text-6xl font-bold">
                  --
                </span>

                <span className="pb-2 text-slate-400">
                  °C
                </span>
              </div>

              <p className="mt-4 text-sm text-slate-400">
                Your trained temperature model will provide tomorrow's
                predicted temperature here.
              </p>
            </motion.section>

            {/* FOOTER */}
            <div className="mt-8 flex flex-col justify-between gap-3 text-sm text-slate-500 md:flex-row">
              <p>
                Data source: {weather.source}
              </p>

              <p>
                Automatically refreshes every 10 minutes
              </p>
            </div>
          </>
        )}

      </div>
    </main>
  );
}


function WeatherCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
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