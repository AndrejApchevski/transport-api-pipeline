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

```bash
pip install psycopg2-binary requests python-dotenv
