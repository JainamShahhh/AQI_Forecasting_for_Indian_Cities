# Short-Term AQI Forecasting for Indian Cities

This project implements a robust machine learning and deep learning pipeline to forecast hour-ahead Air Quality Index (AQI) for major Indian cities. By analyzing historical pollutant data and temporal patterns, the system provides actionable insights for environmental monitoring.

## 1. Project Overview

*   **Objective**: To predict AQI values for the next hour ($t+1$) based on historical pollutant concentrations and time-based features.
*   **Scope**: Covers multiple cities including Delhi, Hyderabad, and Visakhapatnam.
*   **Significance**: Enables proactive warnings for hazardous air quality events, supporting public health and policy decisions.

## 2. Dataset Description

The analysis is based on hourly air quality data from the Central Pollution Control Board (CPCB) and OpenAQ.

*   **`station_hour.csv`**: Contains ~2.5 million hourly readings.
    *   **Key Pollutants**: `PM2.5`, `PM10`, `NO2`, `NH3`, `SO2`, `CO`, `O3`.
    *   **Target Variable**: `AQI` (Air Quality Index).
    *   **Temporal Resolution**: 1 Hour.
*   **`stations.csv`**: Metadata including `StationName`, `City`, `State`, and `Status` (Active/Inactive).

## 3. Methodology

### 3.1 Data Preprocessing
*   **Cleaning**: Removal of invalid station records and handling of missing timestamps.
*   **Imputation**: Linear interpolation is used to fill short gaps in pollutant data to maintain time-series continuity.
*   **Outlier Treatment**: An Interquartile Range (IQR) method is applied to cap extreme pollutant values that may represent sensor errors.

### 3.2 Feature Engineering
We construct a rich feature set to capture the cyclic and persistent nature of air pollution:
*   **Temporal Markers**: `Hour` (diurnal cycle), `Day of Week` (weekend traffic effects), `Month` (seasonal variations).
*   **Lag Features**: Values from previous time steps (`t-1`, `t-6`, `t-24`) to capture persistence.
*   **Rolling Statistics**: Rolling means over 3-hour and 24-hour windows to smooth noise and capture trends.

### 3.3 Modeling Strategy
We compare multiple forecasting approaches:
1.  **Baseline**: Persistence model (predicting $t+1$ is the same as $t$).
2.  **Ensemble Methods**:
    *   **Random Forest Regressor**: Captures non-linear interactions.
    *   **XGBoost Regressor**: Gradient boosting for high performance on tabular data.
3.  **Deep Learning (Sequence Models)**:
    *   **LSTM (Long Short-Term Memory)**: Capable of learning long-term dependencies.
    *   **GRU (Gated Recurrent Unit)**: A computationally efficient variant of LSTM.

## 4. Evaluation & Results

Models are evaluated using a strict **Time-Based Split** (Train on past, Test on future) to prevent data leakage.

*   **Metrics**:
    *   **MAE (Mean Absolute Error)**: Average magnitude of errors.
    *   **RMSE (Root Mean Squared Error)**: Penalizes large prediction errors more heavily.
    *   **R² Score**: Explains the variance captured by the model.

*   **Explainability**: SHAP (SHapley Additive exPlanations) values are generated for the XGBoost model to quantify the impact of each feature (e.g., "How much does high PM2.5 at 8 AM contribute to the predicted AQI?").

## 5. Prerequisites

The project requires Python 3.8+ and the following libraries:

```bash
# Core Data Science
pip install numpy pandas matplotlib seaborn

# Machine Learning
pip install scikit-learn xgboost lightgbm

# Deep Learning
pip install tensorflow

# Interpretability
pip install shap
```

*Note: macOS users (M-series chips) may need `brew install libomp` for XGBoost.*

## 6. Project Structure

```text
├── Final Project File_ENG M 680 (1) (1).ipynb   # Main analysis notebook
├── README.md                                    # Project documentation
├── station_hour.csv                             # Raw hourly data
└── stations.csv                                 # Station metadata
```

## 7. How to Reproduce

1.  **Setup**: Install dependencies listed above.
2.  **Data**: Ensure CSV files are in the root directory.
3.  **Execution**: Open the Jupyter Notebook and select `Run All`.
4.  **Output**: The notebook will generate:
    *   EDA correlation heatmaps.
    *   Loss curves for LSTM/GRU training.
    *   Performance tables comparing all models.
    *   SHAP summary plots for feature importance.
