from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np

# تحميل النموذج عند بداية تشغيل السيرفر
model = joblib.load("milk_model.joblib")

app = FastAPI(
    title="Milk Yield Prediction API",
    description="نظام توقع إنتاج الحليب اليومي لكل بقرة باستخدام الانحدار الخطي متعدد المتغيرات",
    version="1.0.0",
)

# ✅ إضافة CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # يسمح لأي موقع بالوصول (مناسب للتطوير)
    allow_credentials=True,
    allow_methods=["*"],      # يسمح بكل أنواع الطلبات (GET, POST...)
    allow_headers=["*"],      # يسمح بكل الهيدرز
)

# ترتيب الميزات يجب أن يطابق ترتيب التدريب
FEATURE_NAMES = [
    "feed_intake_kg",
    "feed_quality_score",
    "parity",
    "days_in_milk",
    "ambient_temp_C",
    "humidity_pct",
    "body_condition_score",
    "somatic_cell_count",
]

class CowFeatures(BaseModel):
    feed_intake_kg: float = Field(..., description="كمية العلف اليومية (كغ)")
    feed_quality_score: float = Field(..., ge=0.0, le=1.0, description="جودة العلف من 0 إلى 1")
    parity: int = Field(..., ge=1, le=3, description="رقم الولادة (1 للبكائر، 2 أو 3 للأكبر)")
    days_in_milk: int = Field(..., ge=0, description="عدد الأيام منذ بداية موسم الحليب (DIM)")
    ambient_temp_C: float = Field(..., description="درجة الحرارة المحيطة (°C)")
    humidity_pct: float = Field(..., ge=0.0, le=100.0, description="الرطوبة النسبية (%)")
    body_condition_score: float = Field(..., ge=1.0, le=5.0, description="مؤشر حالة جسم البقرة (1-5)")
    somatic_cell_count: float = Field(..., ge=0.0, description="عدّ الخلايا الجسدية SCC")

class PredictionResponse(BaseModel):
    predicted_milk_yield_L: float
    feature_contributions: dict

@app.get("/")
def root():
    return {
        "message": "Milk Yield Prediction API is running.",
        "predict_endpoint": "/predict",
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_milk_yield(features: CowFeatures):
    # تحويل البيانات إلى ترتيب يناسب النموذج
    x = np.array([[
        features.feed_intake_kg,
        features.feed_quality_score,
        features.parity,
        features.days_in_milk,
        features.ambient_temp_C,
        features.humidity_pct,
        features.body_condition_score,
        features.somatic_cell_count,
    ]])

    # توقع إنتاج الحليب
    prediction = model.predict(x)[0]

    # حساب مساهمة كل ميزة تقريبياً (coefficient * value)
    if hasattr(model, "coef_"):
        coefs = model.coef_
        contributions = {
            name: float(coef * value)
            for name, coef, value in zip(
                FEATURE_NAMES, coefs, x[0]
            )
        }
    else:
        contributions = {name: None for name in FEATURE_NAMES}

    return PredictionResponse(
        predicted_milk_yield_L=float(prediction),
        feature_contributions=contributions,
    )
