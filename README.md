        ┌───────────────────┐
        │  Raw Data Sources │
        │                   │
        │ 1. NYC Taxi Data  │
        │    (Parquet)      │
        │                   │
        │ 2. Weather Data   │
        │    (CSV)          │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Bronze Layer      │
        │ (Raw Storage)     │
        │                   │
        │ /bronze/taxi/     │
        │ /bronze/weather/  │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Silver Layer      │
        │ (Cleaned Data)    │
        │                   │
        │ taxi_clean:       │
        │  - Remove invalid │
        │    trips          │
        │  - Extract dates  │
        │  - Trip duration  │
        │ weather_clean:    │
        │  - Keep key cols  │
        │  - Format dates   │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Gold Layer        │
        │ (Analytics-Ready) │
        │                   │
        │ taxi_weather:     │
        │  - Join on date   │
        │  - Aggregate KPI  │
        │    (avg fare,     │
        │     trip count,   │
        │     tips)         │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Analytics         │
        │                   │
        │ - Rain vs Clear   │
        │   day fares       │
        │ - Weather impact  │
        │   on trip count   │
        └───────────────────┘
