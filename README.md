🚖 NYC Taxi + Weather ETL (Databricks + Delta Lake) 
📌 Overview      
ETL pipeline with Databricks, PySpark, Delta Lake     
Combines NYC taxi trip data with daily NYC weather data     
Follows Medallion Architecture → Bronze → Silver → Gold  
🛠 Tech Stack     
Databricks
Apache Spark (PySpark)      
Delta Lake     
Parquet & CSV formats  

Avg fare: rainy vs clear days      
Trip counts by weather condition      
Tip behavior trends 

📁 Data Sources      
NYC Taxi Data – [TLC Trip Records  ](https://www.nyc.gov/assets/tlc/pages/about/tlc-trip-record-data)   
Weather Data – [NOAA Climate Data](https://www.ncdc.noaa.gov/cdo-web/)

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
