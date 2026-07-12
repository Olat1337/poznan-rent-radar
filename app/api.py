import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "catboost_housing_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "model_features.pkl")

model = None
model_features = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, model_features
    model = joblib.load(MODEL_PATH)
    model_features = joblib.load(FEATURES_PATH)
    yield

app = FastAPI(title="Poznań Real Estate Rent Predictor API", lifespan=lifespan)

DISTRICT_MAP = {
    'Jeżyce': 'City_Center', 'Stare Miasto': 'City_Center', 'Centrum': 'City_Center',
    'Wilda': 'Mid_Tier', 'Grunwald': 'Mid_Tier', 'Nowe Miasto': 'Mid_Tier', 'Rataje': 'Mid_Tier',
    'Winogrady': 'Mid_Tier', 'Łacina': 'Mid_Tier',
    'Naramowice': 'Outskirts', 'Piątkowo': 'Outskirts', 'Świerczewo': 'Outskirts',
    'Junikowo': 'Outskirts', 'Kasztelanów': 'Outskirts', 'Podolany': 'Outskirts'
}

class ApartmentFeatures(BaseModel):
    area: float = Field(..., ge=15, le=120)
    floor_num: int = Field(..., ge=-1, le=12)
    rooms_num: int = Field(..., ge=1, le=7)
    has_ac: bool
    has_balcony: bool
    has_terrace: bool
    has_parking: bool
    has_storage: bool
    is_secure: bool
    location: str

@app.get("/")
def home():
    return {"message": "API is online. Send a POST request to /predict to get a rental estimate."}

@app.post("/predict")
def predict_rent(features: ApartmentFeatures):
    try:
        user_district = DISTRICT_MAP.get(features.location, 'Other')

        input_data = {
            "area": features.area,
            "floor_num": features.floor_num,
            "rooms_num": features.rooms_num,
            "has_ac": int(features.has_ac),
            "has_balcony": int(features.has_balcony),
            "has_terrace": int(features.has_terrace),
            "has_parking": int(features.has_parking),
            "has_storage": int(features.has_storage),
            "is_secure": int(features.is_secure),
            f"location_{features.location}": 1,
            f"district_category_{user_district}": 1
        }

        input_df = pd.DataFrame([input_data])
        input_df = input_df.reindex(columns=model_features, fill_value=0)

        log_prediction = model.predict(input_df)
        estimated_price_pln = float(np.exp(log_prediction)[0])

        return {"predicted_fair_rent_pln": round(estimated_price_pln, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")