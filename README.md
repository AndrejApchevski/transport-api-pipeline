# 🚌 Transport API Data Ingestion Pipeline

This project builds a data ingestion pipeline to fetch live bus departure data from the TransportAPI, store it in a PostgreSQL database, and collect hourly data over a period (planned for one month) for later analysis.

---

## 🚀 Project Overview

- Fetches real-time bus live data from TransportAPI for a specific bus stop (ATCO code: `490000235Z`, New Oxford Street, London).  
- Data is ingested every hour using a Python script.  
- Data is stored in a PostgreSQL database with timestamps to enable time-series analysis.  
- Designed to collect at least one month of data to allow analysis of trends, peak hours, delays, and other operational insights.

---

## ✨ Features

- 🔐 Uses environment variables to securely store API credentials (`APP_ID` and `APP_KEY`) in a `.env` file.  
- 🔗 Connects to TransportAPI with API keys and fetches bus departure information grouped by bus line.  
- 💾 Inserts data into a PostgreSQL table (`bus_live_data`) including a `fetched_at` timestamp to track data collection time.  
- ⏰ Script run is automated via a Windows Task Scheduler `.bat` file to execute hourly.  
- ⚠️ Error handling included for API request failures and database connection issues.

---

## 🛠️ Setup Instructions

### 📋 Prerequisites

- 🐍 Python 3.11+ installed  
- 🐘 PostgreSQL 17 installed and running locally  
- 📦 Python packages installed: `psycopg2-binary`, `requests`, `python-dotenv`  
- 🐙 Git installed (optional for version control)

### 📦 Install Python packages

bash
pip install psycopg2-binary requests python-dotenv

🗄️ Database Setup
Create a PostgreSQL database named transport_data.

Create the table bus_live_data with this schema:

sql
Copy
Edit
CREATE TABLE IF NOT EXISTS bus_live_data (
    id SERIAL PRIMARY KEY,
    line_name VARCHAR(50),
    direction VARCHAR(100),
    aimed_departure TIME,
    expected_departure TIME,
    operator_name VARCHAR(100),
    stop_name VARCHAR(100),
    atcocode VARCHAR(50),
    fetched_at TIMESTAMP
);
Make sure the database user (e.g., postgres) has proper permissions.

🔑 Environment Variables
Create a .env file in the root project folder:

ini
Copy
Edit
APP_ID=your_transportapi_app_id
APP_KEY=your_transportapi_app_key
Add .env to .gitignore to avoid committing sensitive information.

🐍 Python Script
The main ingestion script is fetch_live_data_hourly.py.

This script fetches live bus data and inserts it into PostgreSQL.

Make sure the script is in the scripts folder (or update paths accordingly).

⚙️ Automation with Windows Task Scheduler
Create a .bat file (run_transport_api.bat) in the project root:

bat
Copy
Edit
@echo off
cd /d "C:\Users\PC\transport-api-pipeline\scripts"
"C:\Users\PC\AppData\Local\Programs\Python\Python311\python.exe" fetch_live_data_hourly.py
Schedule this .bat file to run every hour using Windows Task Scheduler (see project documentation).

📊 Data Collection Plan
The pipeline fetches 15 bus departure records every hour.

Planned to collect data for at least one month to analyze:

Daily & weekly trends

Peak usage hours

Delay patterns

Anomaly detection

🔜 Next Steps
Perform exploratory data analysis (EDA) after initial data collection.

Build dashboards or visualizations (Power BI, Tableau, or Python matplotlib/seaborn).

Develop predictive models for bus delays or ridership forecasting.

Extend the project to include multiple bus stops or other transport modes.

🛠️ Troubleshooting
If the script fails, check:

Your .env file contains correct API keys.

PostgreSQL server is running and accessible.

Required Python packages are installed (requests, psycopg2-binary, python-dotenv).

Paths in the .bat file are correct.

📄 License
This project is open-source and free to use.

Created by Andrej Apchevski
