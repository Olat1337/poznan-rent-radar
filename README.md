# 🏡 Poznań Rent Radar: Real Estate Valuation Engine

An end-to-end machine learning and data application that predicts fair market rental prices for apartments in Poznań, Poland. 

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41+-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.5+-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.2+-150458.svg?logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-2.1+-013243.svg?logo=numpy)](https://numpy.org/)
## 🔗 Live Demo
* **Frontend UI (Streamlit):** https://poznan-rent-radar-ui.up.railway.app/
* **Backend API (FastAPI):** https://poznan-rent-radar-api.up.railway.app/docs

---

## 🎯 Project Overview
Finding an apartment can be stressful, and knowing if a listing is fairly priced is a constant challenge. **Poznań Rent Radar** solves this by scraping live real estate listings, processing the data, and using an AI algorithm to calculate the true market value of an apartment based on its structural dimensions, location, and premium amenities.

This project was built from scratch to demonstrate a complete, production-ready Data Science lifecycle-from web scraping and Exploratory Data Analysis (EDA) to Machine Learning and cloud deployment.

---

## 🛠️ Full Technology Stack

To ensure high availability, accurate analysis, and fast performance, the application utilizes a modern Python data ecosystem and a decoupled microservices architecture.

### Data Engineering & EDA
* **Pandas & NumPy:** For rigorous data manipulation, cleaning, and numerical transformations.
* **Seaborn & Matplotlib:** For generating visual market insights, detecting outliers, and mapping feature distributions.
* **Python Built-ins (`ast`, `re`):** Used extensively for safely evaluating nested JSON strings and dynamically parsing Next.js build IDs during web scraping.

### Machine Learning
* **Scikit-Learn:** Built and tuned a Random Forest Regressor featuring Natural Log Transformations and leak-free Train/Test splits.
* **Joblib:** For efficient serialization and deserialization of the trained `.pkl` models into the backend.

### Full-Stack Architecture
* **Backend Engine (FastAPI & Uvicorn):** A high-performance REST API utilizing **Pydantic** for strict data validation and request routing.
* **Presentation Layer (Streamlit & Requests):** A responsive web interface that consumes the API and displays predictions.
* **CI/CD Cloud Deployment (Railway):** Both services are deployed independently using Railway's native Nixpacks build engine to prevent port-racing conditions.

---
## 📊 Data & Modeling Workflow

Before deployment, data exploration and model training were completed in `notebooks/EDA_and_Cleaning.ipynb`:

* **Data Cleaning:** Parsed nested string JSON structures and calculated `true_price` (Total Rent + Admin Rent).
* **Feature Encoding:** Converted text layout descriptions (e.g., `"GROUND"`, `"FIRST"`) into sequential integer mapping.
* **Outlier Removal:** Filtered entries outside realistic ranges (15-120 sqm, 1,200-8,000 PLN) to eliminate human errors.
* **Leakage Mitigation:** Split data 80/20 and imputed missing values using the median derived strictly from the training set.
* **Log Transformation:** Stabilized right-skewed pricing targets by fitting the model on the natural log (`np.log`) of the rent.
---
## 📁 Repository Structure

```text
├── .streamlit/                
│   └── config.toml            # UI Theme Configuration
├── app/
│   ├── api.py                 # FastAPI backend implementation
│   └── ui.py                  # Streamlit frontend user interface
├── models/
│   ├── model_features.pkl     # Saved One-Hot Encoded feature columns
│   └── poznan_rent_model.pkl  # Trained Random Forest Regressor
├── notebooks/
│   └── EDA_and_Cleaning.ipynb # Data cleaning, EDA, and model training workflow
├── src/
│   └── parser.py              # Dynamic Next.js scraper logic
├── requirements.txt           # Frozen production dependencies
├── .gitignore                 # Configures files and directories to ignore in Git
└── README.md                  # Project documentation
(Note: Raw scraped data and local log files are intentionally git-ignored to maintain clean version control hygiene).
```
## 📈 Model Performance
Algorithm: Random Forest Regressor

Validation MAE: ~337 PLN (The model predicts the monthly rent within an average margin of error of 340 PLN compared to reality).

Key Insights: Feature importance analysis revealed that physical area dictates 55% of pricing weight, followed closely by central location premiums (e.g., Jeżyce, Stare Miasto).
## 🚀 How to Run Locally
If you would like to run this application on your own machine, follow these steps:

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
In your first terminal, spin up the FastAPI server:
```Bash
uvicorn app.api:app --reload --port 8080
```
4. Start the Frontend UI
Open a second terminal, inject the local API URL, and start Streamlit:
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