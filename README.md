# 🏡 Poznań Rent Radar: Real Estate Valuation Estimator

A machine learning project that estimates fair market rental prices for apartments in Poznań, Poland.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![CatBoost](https://img.shields.io/badge/CatBoost-1.2+-yellow.svg)](https://catboost.ai/)
[![Optuna](https://img.shields.io/badge/Optuna-3.6+-blue.svg)](https://optuna.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.2+-150458.svg?logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-2.1+-013243.svg?logo=numpy)](https://numpy.org/)

## 🔗 Live Demo
* **Frontend UI (Streamlit):** https://poznan-rent-radar-ui.up.railway.app
* **Backend API (FastAPI):** https://poznan-rent-radar-api.up.railway.app/docs

<img width="1920" height="1080" alt="Poznan Rent Radar UI GIF" src="https://github.com/user-attachments/assets/5708b1fc-0119-4be3-b9ec-63ed3bfb7e66" />

## 🎯 Project Overview
I built this project to learn and demonstrate a complete machine learning pipeline-from data collection to web deployment. 

The application scrapes real estate listings, processes the data, and uses a trained model to estimate the rental value of an apartment based on features like area, location, and amenities. 

## 🛠️ Technology Stack & Architecture Decisions

I split this application into a decoupled backend API and a frontend UI.

### Data Engineering & Modeling
* **Stack:** Python, Pandas, NumPy, Scikit-Learn, CatBoost, Optuna.
* **Why this stack:** Standard, well-documented tools for data cleaning and transformation. Optuna is fantastic for automated, highly efficient hyperparameter tuning.
* **Why CatBoost:** After benchmarking on log-transformed prices and testing Random Forest, LightGBM, XGBoost, and a combined Voting Ensemble model, pure CatBoost achieved the best overall accuracy (lowest MAE) on this specific dataset without overfitting.

### Web Frameworks & Deployment
* **Backend:** FastAPI.
* **Frontend:** Streamlit.
* **Why decouple them:** Separating the ML inference API from the UI makes the application easier to test locally and allows each service to be restarted or debugged independently. I chose Streamlit because it allows for rapid UI prototyping for data apps.
* **Deployment:** Automated CI/CD on Railway.
* **Why Railway:** It offers a straightforward platform for deploying independent Docker/Nixpacks containers directly from GitHub, preventing port conflicts between the API and the UI.

## 📊 Data & Modeling Workflow

Before deployment, data exploration and model training were broken down into a clear, step-by-step pipeline located in the `notebooks/` folder:

* **`1_EDA_and_Cleaning.ipynb`:** Cleaned the raw scraped JSON data, calculated `true_price` (Total + Admin Rent), and removed extreme outliers (filtered to 15-120 sqm and 1,200-8,000 PLN). Converted categories using One-Hot Encoding and ordinal mapping.
* **`2_Finding_best_hyperparams.ipynb`:** Applied a safe log transformation (`np.log1p`) to stabilize right-skewed pricing distributions. Ran 200 optimization trials per algorithm using Optuna to find the absolute best model parameters.
* **`3_ML_training.ipynb`:** Safely split the data 80/20 and prevented data leakage by imputing missing values strictly using the training set median. Trained and evaluated Random Forest, LightGBM, XGBoost, CatBoost, and an Ensemble model. 
* **`4_Conclusion_Evaluation_and_Feature_Importance.ipynb`:** Extracted feature importances (discovered `area` is the dominant price driver). Visualized actual vs. predicted errors to design a safety guardrail for the UI.

## 📈 Model Performance & Safety
* **Algorithm:** CatBoost Regressor.
* **Validation MAE:** ~307 PLN. This means the model's estimates are, on average, within 307 PLN of the actual listed rental price.

## 📁 Repository Structure

```text
├── .streamlit/                
│   └── config.toml            # UI Theme Configuration
├── app/
│   ├── api.py                 # FastAPI backend endpoints
│   └── ui.py                  # Streamlit frontend layout
├── models/
│   ├── model_features.pkl         # Saved One-Hot Encoded feature columns
│   └── catboost_housing_model.pkl # Trained CatBoost Regressor
├── notebooks/
│   ├── 0_Project_Overview.ipynb
│   ├── 1_EDA_and_Cleaning.ipynb 
│   ├── 2_Finding_best_hyperparams.ipynb
│   ├── 3_ML_training.ipynb
│   └── 4_Conclusion_Evaluation_and_Feature_Importance.ipynb
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

On Mac/Linux:

```Bash
export BACKEND_URL="http://127.0.0.1:8080"
streamlit run app/ui.py
```
On Windows (PowerShell):
```Bash
$env:BACKEND_URL="http://127.0.0.1:8080"
streamlit run app/ui.py
```
The UI will automatically open in your browser at http://localhost:8501.
