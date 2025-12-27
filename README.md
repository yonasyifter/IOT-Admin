# IoT Environmental Monitoring (Django + InfluxDB + DRF + Vue.js)

An end-to-end **IoT environmental monitoring** platform to collect, store, and visualize sensor data (e.g., temperature, humidity, CO₂, PM2.5).  
The backend is built with **Django + Django REST Framework**, time-series data is stored in **InfluxDB**, and the dashboard UI is built with **Vue.js**.

---

## Features

- ✅ Device registration & management (multiple IoT nodes)
- ✅ Secure REST APIs (JWT/session auth depending on your setup)
- ✅ Time-series storage using InfluxDB (fast writes + efficient range queries)
- ✅ Dashboard for live and historical charts (Vue.js)
- ✅ Filtering by device, metric, time range
- ✅ Aggregations (min/max/avg) for selected windows (optional)
- ✅ Alerts/thresholds (optional if implemented)

---

## Tech Stack

### Backend
- **Python / Django**
- **Django REST Framework (DRF)**
- **InfluxDB** (time-series database)

### Frontend
- **Vue.js** (Vite / Vue CLI)
- Charting library (e.g., Chart.js / ECharts — update based on what you used)

---

## High-Level Architecture

```text
[IoT Sensors/Devices]
        |
        |  HTTP / MQTT (optional)  + JSON/Line Protocol
        v
   [Django + DRF API]  ----->  [InfluxDB]
        |
        |  REST API (auth + queries)
        v
   [Vue.js Dashboard]
