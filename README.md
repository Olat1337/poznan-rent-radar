# 🏢 Poznań Real Estate Rent Predictor

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-009688.svg?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.26+-FF4B4B.svg?logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E.svg?logo=scikit-learn&logoColor=white)

An end-to-end Machine Learning system that scrapes live real estate data, processes features via a hardened pipeline, and serves an optimized rent prediction model through an interactive web dashboard.

## ⚙️ Tech Stack
* **Data & ML:** Pandas, NumPy, Scikit-Learn (Random Forest), Joblib
* **Backend:** FastAPI, Pydantic, Uvicorn, Requests
* **Frontend:** Streamlit

## 🛠️ System Architecture & Performance
1. **Data Pipeline (`src/parser.py` & `notebooks/`):** Next.js pagination scraper with defensive error handling, followed by strict EDA, target log-transformations (`np.log`), and anti-leakage train/test splits.
2. **Inference API (`app/api.py`):** Asynchronous FastAPI backend that dynamically processes structural inputs and one-hot encoded geographical dummy variables.
3. **Interactive UI (`app/ui.py`):** Reactive Streamlit dashboard connecting end-users to the real-time inference engine.
* **Model Benchmark:** Optimized Random Forest Regressor achieving a **397.91 PLN MAE**. (Primary price drivers: Area ~60%, Room Count, and District premium weights).

## 🚀 Quick Start
Ensure you have Python 3.11+ installed. Clone this repository and run:

```bash
pip install -r requirements.txt
uvicorn app.api:app --reload   # Terminal Window 1: Starts the API
streamlit run app/ui.py        # Terminal Window 2: Starts the UI