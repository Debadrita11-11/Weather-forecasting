# Weather Intelligence & Forecasting System

An end-to-end Machine Learning based weather forecasting project designed to predict temperature and provide real-time weather information through an interactive web dashboard.

## Project Overview

This project uses historical Kolkata weather data (2017–2026) to train and evaluate Machine Learning models for temperature forecasting. It also integrates live weather information through the Visual Crossing Weather API.

## Key Features

- Historical weather data analysis
- Data preprocessing and feature engineering
- Temperature prediction using Machine Learning
- Actual vs Predicted temperature visualization
- Model evaluation using MAE, RMSE and R²
- Real-time weather updates
- Interactive web dashboard
- FastAPI backend integration

## Technologies Used

**Programming:** Python, JavaScript

**Machine Learning:** Scikit-learn, Pandas, NumPy

**Visualization:** Matplotlib

**Backend:** FastAPI

**Frontend:** Next.js, React

**API:** Visual Crossing Weather API

**Deployment:** Render

## Machine Learning Models

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

## Dataset

Historical Kolkata weather data covering 2017–2026.

## Model Performance

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 1.114 | 1.465 | 0.874 |
| Random Forest | 1.164 | 1.511 | 0.866 |
| Gradient Boosting | 1.156 | 1.493 | 0.869 |

Linear Regression achieved the lowest RMSE among the evaluated models.

## Project Structure

- `data/` – Historical weather dataset
- `models/` – Trained ML models
- `src/` – Backend and model code
- `dashboard/` – Frontend dashboard

## Future Improvements

- Improve forecasting accuracy
- Integrate additional weather parameters
- Enhance dashboard visualizations
- Deploy a fully accessible live application

## Author

Data Science Student | Machine Learning & Web Development Enthusiast
