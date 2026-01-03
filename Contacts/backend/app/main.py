

from pyexpat import model
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# تحميل النموذج المدرب
model = joblib.load("milk_yield_model.pkl")

# تعريف شكل البيانات المدخلة
class CowData(BaseModel):
    feed_intake_kg: float
    feed_quality_score: float
    parity: int
    days_in_milk: int
    ambient_temp_C: float
    humidity_pct: float
    body_condition_score: float
    somatic_cell_count: float

@app.post("/predict")
def predict_milk_yield(data: CowData):
    features = np.array([[data.feed_intake_kg,
                          data.feed_quality_score,
                          data.parity,
                          data.days_in_milk,
                          data.ambient_temp_C,
                          data.humidity_pct,
                          data.body_condition_score,
                          data.somatic_cell_count]])
    prediction = model.predict(features)
    return {"milk_yield_L": round(prediction[0], 2)}
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/weather")
def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url).json()
    temp = response["current_weather"]["temperature"]
    humidity = response["current_weather"]["relativehumidity"]
    return {"temperature": temp, "humidity": humidity}
