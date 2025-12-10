# System Architecture & Deployment Vision

This document outlines the architectural design of the AQI Forecasting System, including data flow, model pipeline, and future deployment strategies.

## 1. High-Level Architecture

The system is designed as a modular pipeline that ingests raw pollutant data, processes it into temporal features, and generates hourly forecasts using ensemble machine learning models.

```mermaid
graph TD
    A[Raw Data Sources] -->|Station API/CSV| B(Data Ingestion Layer)
    B --> C{Preprocessing Engine}
    C -->|Impute & Clean| D[Feature Engineering]
    D -->|Lags & Rolling Utils| E[Model Inference]
    E -->|XGBoost/RF| F[AQI Forecast]
    F --> G[Dashboard / API]
    G --> H[End User]
    
    subgraph "Preprocessing & Features"
    C
    D
    end
    
    subgraph "AI Core"
    E
    F
    end
```

## 2. Data Pipeline

1.  **Ingestion**: 
    *   **Historical**: CPCB/OpenAQ archives (CSV).
    *   **Live (Future)**: Real-time REST API polling from monitoring stations.
2.  **Processing**:
    *   **Cleaning**: Outlier removal using IQR.
    *   **Enrichment**: Merging with synthetic or API-based meteorological data (Temperature, Wind).
3.  **Featurization**:
    *   Creation of `AQI_lag_1`, `AQI_lag_24` to capture daily cycles.
    *   Rolling averages to smooth volatile sensor readings.

## 3. Next Steps & Deployment

 To move from this research notebook to a production system, we propose the following roadmap:

### Phase 1: API Development (`FastAPI`)
*   Wrap the trained XGBoost model in a Python FastAPI service.
*   Endpoint: `POST /predict` accepting `StationID` and recent pollutant history.

### Phase 2: Automated Retraining (`Airflow`)
*   Implement an Airflow DAG to retrain the model weekly using the latest data to handle concept drift (seasonality changes).

### Phase 3: User Dashboard (`Streamlit/React`)
*   Build a frontend to visualize:
    *   Current AQI Heatmap.
    *   6-Hour Forecast Curve.
    *   Health Advisories based on predicted AQI buckets.

## 4. Integration Diagram

```mermaid
sequenceDiagram
    participant User
    participant Dashboard
    participant API
    participant ModelRegistry
    
    User->>Dashboard: View Forecast for "Delhi"
    Dashboard->>API: GET /forecast?city=Delhi
    API->>ModelRegistry: Load Latest XGBoost Model
    API->>API: Compute Features (Lags, Weather)
    API-->>Dashboard: Return JSON { "hour_1": 350, "hour_2": 345 ... }
    Dashboard-->>User: Display Forecast Graph
```
