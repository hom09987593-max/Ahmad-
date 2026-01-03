from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib
import pandas as pd
import numpy as np
import requests
 

 


app = FastAPI()


# 1. إعدادات CORS (للسماح بالاتصال من CodeSandbox والفرونت إند)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. تحميل النماذج (Model Loading)
try:
    # النموذج الأول (كما في الكود الأول)
    model_pkl = joblib.load("../../ai/milk_model_custom.joblib") 
except:
    model_pkl = None
    print("Warning: milk_model_custom.joblib not found!")

try:
    # النموذج الثاني (كما في الكود الثاني)
    model_joblib = joblib.load("../../ai/milk_model.joblib")
except:
    model_joblib = None
    print("Warning: milk_model.joblib not found!")

# 3. تعريف نماذج البيانات (Pydantic Models)
class CowData(BaseModel):
    feed_intake_kg: float
    feed_quality_score: float
    parity: int
    days_in_milk: int
    ambient_temp_C: float
    humidity_pct: float
    body_condition_score: float
    somatic_cell_count: float

class PredictionInput(BaseModel):
    Animal_ID: int
    Age: int
    Weight: float
    Milk_Yield_Day_1: float
    Milk_Yield_Day_2: float

# 4. المسارات (Routes)

@app.get("/")
def home():
    return {"status": "Online", "message": "Backend is connected successfully!"}

@app.get("/api/data")
def get_data():
    return{"items":["AI Model 1","AI Model 2","AI Model 3"]}

# مسار التوقع الأول (CowData)
@app.post("/predict_yield_detailed")
def predict_milk_yield(data: CowData):
    if model_pkl is None:
        return {"error": "Detailed model not loaded"}
    features = np.array([[data.feed_intake_kg,
                          data.feed_quality_score,
                          data.parity,
                          data.days_in_milk,
                          data.ambient_temp_C,
                          data.humidity_pct,
                          data.body_condition_score,
                          data.somatic_cell_count]])
    prediction = model_pkl.predict(features)
    return {"milk_yield_L": round(prediction[0], 2)}

# مسار التوقع الثاني (PredictionInput)
@app.post("/predict")
def predict(data: PredictionInput):
    if model_joblib is None:
        return {"error": "Main model not loaded"}
    input_df = pd.DataFrame([data.dict()])
    prediction = model_joblib.predict(input_df)
    return {"prediction": float(prediction[0])}


# مسار الطقس
@app.get("/weather")
def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url).json()
    # ملاحظة: استجابة Open-Meteo قد تختلف أسماء الحقول فيها أحياناً
    current = response.get("current_weather", {})
    temp = current.get("temperature")
    # الرطوبة غالباً تكون في حقول الـ hourly في هذا الـ API ولكن سنبقي المنطق كما وضعته
    return {"temperature": temp, "message": "Weather data fetched"}