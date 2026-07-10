# 🏡 Poznań Rent Radar: Real Estate Valuation Estimator

A machine learning project that estimates fair market rental prices for apartments in Poznań, Poland.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.2+-150458.svg?logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-2.1+-013243.svg?logo=numpy)](https://numpy.org/)

## 🔗 Live Demo
* **Frontend UI (Streamlit):** https://poznan-rent-radar-ui.up.railway.app
* **Backend API (FastAPI):** https://poznan-rent-radar-api.up.railway.app/docs

<img width="1920" height="1080" alt="Poznan Rent Radar GIF" src="https://github.com/user-attachments/assets/b02687b7-6a15-4844-acec-bde6063a1b99" />

## 🎯 Project Overview
I built this project to learn and demonstrate a complete machine learning pipeline—from data collection to web deployment. 

The application scrapes real estate listings, processes the data, and uses a trained model to estimate the rental value of an apartment based on features like area, location, and amenities. 

## 🛠️ Technology Stack & Architecture Decisions

I split this application into a decoupled backend API and a frontend UI.

### Data Engineering & Modeling
* **Stack:** Python, Pandas, NumPy, Scikit-Learn.
* **Why this stack:** Standard, well-documented tools for data cleaning, transformation, and model building.
* **Why Random Forest:** I chose a Random Forest model over linear models after benchmarking on log-transformed prices because it was much better at handling non-linear feature interactions in real estate pricing.

### Web Frameworks & Deployment
* **Backend:** FastAPI.
* **Frontend:** Streamlit.
* **Why decouple them:** Separating the ML inference API from the UI makes the application easier to test locally and allows each service to be restarted or debugged independently. I chose Streamlit because it allows for rapid UI prototyping for data apps.
* **Deployment:** Automated CI/CD on Railway.
* **Why Railway:** It offers a straightforward platform for deploying independent Docker/Nixpacks containers directly from GitHub, preventing port conflicts between the API and the UI.

## 📊 Data & Modeling Workflow

Before deployment, data exploration and model training were completed in `notebooks/EDA_and_Cleaning.ipynb`:

* **Data Cleaning:** Parsed nested JSON strings to calculate `true_price` (Total Rent + Admin Rent).
* **Feature Engineering:** Applied one-hot encoding for categorical variables and converted text layout descriptions (e.g., `"GROUND"`, `"FIRST"`) into sequential integer mapping.
* **Outlier Removal:** Filtered entries outside realistic bounds (15-120 sqm, 1,200-8,000 PLN) to remove parsing errors and bad listings.
* **Log Transformation:** Applied log transforms to target prices to stabilize right-skewed pricing distributions.
* **Leakage Mitigation:** Split data 80/20 and imputed missing values using the median derived strictly from the training set.

## 📈 Model Performance
* **Algorithm:** Random Forest Regressor.
* **Validation MAE:** ~337 PLN. This means the model's estimates are, on average, within 337 PLN of the actual listed rental price.

## 📁 Repository Structure

```text
├── .streamlit/                
│   └── config.toml            # UI Theme Configuration
├── app/
│   ├── api.py                 # FastAPI backend endpoints
│   └── ui.py                  # Streamlit frontend layout
├── models/
│   ├── model_features.pkl     # Saved One-Hot Encoded feature columns
│   └── poznan_rent_model.pkl  # Trained Random Forest Regressor
├── notebooks/
│   └── EDA_and_Cleaning.ipynb # Data cleaning, EDA, and training workflow
├── src/
│   └── parser.py              # Scraper logic
├── requirements.txt           # Environment dependencies
├── .gitignore                 
└── README.md                  

(Note: Raw scraped data and local log files are git-ignored).
```

## 🚀 How to Run Locally

1. Clone the repository
```Bash
git clone https://github.com/Olat1337/poznan-rent-radar.git
cd poznan-rent-radar
```

2. Install dependencies
```Bash
pip install -r requirements.txt
```

3. Start the Backend API
In your first terminal, start the FastAPI server:
```Bash
uvicorn app.api:app --reload --port 8080
```

4. Start the Frontend UI
Open a second terminal, set the local API URL environment variable, and start Streamlit:
  
  *On Mac/Linux:*
  ```Bash
  export BACKEND_URL="http://127.0.0.1:8080"
  streamlit run app/ui.py
  ```
  
  *On Windows (PowerShell):*
  ```Bash
  $env:BACKEND_URL="http://127.0.0.1:8080"
  streamlit run app/ui.py
  ```
  The UI will automatically open in your browser at `http://localhost:8501`.
