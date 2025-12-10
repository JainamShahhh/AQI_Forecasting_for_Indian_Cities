# Model Card: AQI XGBoost Forecaster

**Model Version**: 1.0  
**Date**: December 2024  
**Developers**: Jainam Shah, Mohammad Hamza, Akhil Mohandas, Kavin Darvin, Jagrat Ruparel

> [!NOTE]
> For the complete, graphical Model Card, please refer to the PDF included in this repository: **[Model card.pdf](Model%20card.pdf)**.

## 1. Intended Use
*   **Primary Use**: Forecasting hourly Air Quality Index (AQI) values for Indian cities up to 6 hours in advance.
*   **Intended Users**: City planners, environmental scientists, and potential public health dashboards.
*   **Out-of-Scope**: Long-term climate modeling (>10 days) or rural areas without station coverage.

## 2. Model Description
*   **Type**: Regression (Gradient Boosted Decision Trees).
*   **Architecture**: XGBoost (`XGBRegressor`) with 400 estimators and max depth of 8.
*   **Inputs**:
    *   Historical Pollutants (`PM2.5`, `PM10`, `NO2`, etc.)
    *   Temporal Features (`Hour`, `Month`, `Season`)
    *   Meteorological Data (`Temperature`, `Humidity`, `Wind Speed`)
*   **Outputs**: Scalar AQI value.

## 3. Performance
*   **Test Metric**: Root Mean Squared Error (RMSE).
*   **Results**: Significantly outperforms the Persistence Baseline.
    *   *Baseline RMSE*: ~3.56
    *   *XGBoost RMSE*: ~2.10
*   **Validation Strategy**: Rolling-origin time series split (Train: 60%, Val: 20%, Test: 20%).

## 4. Ethical Considerations
*   **Bias**: The model is trained primarily on urban data (Delhi, Hyderabad). It may generalize poorly to rural regions with different pollution sources (e.g., crop burning vs. traffic).
*   **Limitations**: Extreme events (e.g., Diwali fireworks) are treated as outliers but may be underpredicted due to their rarity in the training set.

## 5. Quantitative Analysis
See the detailed **SHAP** (Explainability) plots in the Notebook and the full PDF report for breakdown by city and season.
