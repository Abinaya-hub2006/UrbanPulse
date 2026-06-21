# UrbanPulse - Event-Aware Traffic Intelligence Platform

## Overview

UrbanPulse is an AI-powered traffic intelligence platform designed to address event-driven congestion in urban environments. The system analyzes historical traffic incident data, forecasts event impact, recommends resource deployment, suggests diversion routes, and continuously improves through post-event learning.

The solution was developed for the Flipkart GRiD Hackathon challenge focused on Event-Driven Congestion Management.

---

## Problem Statement

Urban traffic networks are frequently disrupted by:

* Political rallies
* Public gatherings
* Festivals
* Sports events
* Construction activities
* VIP movements
* Accidents and emergency situations

Current traffic management systems face several challenges:

* Event impact is not quantified in advance
* Resource deployment is experience-driven
* Diversion planning is reactive
* No post-event learning mechanism exists

UrbanPulse addresses these challenges through predictive analytics and intelligent decision support.

---

## Key Features

### Risk Discovery Engine

Identifies congestion-prone junctions using historical event and incident data.

**Technology Used**

* K-Means Clustering
* Risk Profiling
* Geospatial Analysis

**Outputs**

* Junction Risk Levels
* Hotspot Detection
* Risk Heatmaps

---

### Resource Recommendation Engine

Recommends manpower and barricade deployment based on predicted event severity.

**Outputs**

* Officer Allocation
* Barricade Requirements
* Response Priority Level

---

### Event Impact Forecasting

Forecasts traffic disruption before an event occurs.

**Technology Used**

* Random Forest Regressor
* Historical Event Intelligence

**Model Performance**

* R² Score: 0.867
* Mean Absolute Error: 1.229

**Inputs**

* Event Type
* Crowd Size
* Duration
* Risk Level

**Outputs**

* Predicted Impact Score
* Resource Requirements

---

### Diversion Planning Engine

Suggests low-risk alternative routes for affected traffic corridors.

**Technology Used**

* Geospatial Distance Analysis
* Junction Risk Intelligence

**Outputs**

* Recommended Diversions
* Alternative Junctions
* Diversion Maps

---

### Live Event Feed

Monitors active and upcoming city events and automatically evaluates operational impact.

**Examples**

* Political Rallies
* Public Events
* Construction Activities
* VIP Movements
* Sports Events

---

### Post-Event Learning Engine

Allows operators to submit event outcomes after completion.

The system stores operational feedback and supports model retraining to continuously improve prediction quality.

**Capabilities**

* Event Review Collection
* Historical Learning
* Model Retraining

---

## System Architecture

Historical Event Data
↓
Risk Discovery Engine (K-Means)
↓
Impact Forecasting (Random Forest)
↓
Resource Recommendation
↓
Diversion Planning
↓
Live Event Monitoring
↓
Post-Event Learning
↓
Model Retraining

---

## Technology Stack

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* K-Means Clustering
* Random Forest Regressor

### Visualization

* Plotly
* Folium
* Streamlit Folium

### Deployment

* GitHub
* Streamlit Community Cloud

---

## Dataset

The solution utilizes historical urban traffic event data containing:

* Event Causes
* Priority Levels
* Road Closures
* Incident Locations
* Event Categories
* Operational Information

The dataset is transformed into risk intelligence and forecasting datasets for model training.

---

## Project Structure

```text
UrbanPulse/
│
├── app.py
│
├── data/
│   ├── Astram_event_data.csv
│   ├── junction_risk_table.csv
│   ├── live_events.csv
│   └── post_event_reviews.csv
│
├── models/
│   ├── junction_risk_model.pkl
│   ├── impact_model.pkl
│   ├── event_encoder.pkl
│   └── risk_encoder.pkl
│
├── modules/
│   ├── risk_module.py
│   ├── resource_module.py
│   ├── simulator_module.py
│   ├── diversion_module.py
│   ├── learning_module.py
│   └── retraining_module.py
│
└── requirements.txt
```

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## Future Enhancements

* Real-time traffic API integration
* Weather-aware congestion forecasting
* Graph-based route optimization
* Automated event feed ingestion
* Smart city command center integration

---

## Impact

UrbanPulse transforms traffic management from reactive operations to proactive intelligence.

The platform enables authorities to:

* Predict congestion before it occurs
* Optimize resource deployment
* Reduce response time
* Improve traffic flow
* Learn continuously from completed events

---

## Team

Developed as part of the Flipkart GRiD Hackathon submission.

UrbanPulse — Predict. Plan. Prevent. Learn.
