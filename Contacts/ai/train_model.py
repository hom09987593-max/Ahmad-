import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def generate_synthetic_data(n_samples: int = 1000, random_state: int = 42):
    np.random.seed(random_state)

    # feed_intake_kg: كمية العلف (من 10 إلى 30 كغ)
    feed_intake_kg = np.random.uniform(10, 30, n_samples)

    # feed_quality_score: جودة العلف (0 إلى 1)
    feed_quality_score = np.random.uniform(0, 1, n_samples)

    # parity: رقم الولادة (1, 2, 3)
    parity = np.random.choice([1, 2, 3], size=n_samples)

    # days_in_milk: من 10 إلى 300 يوم
    days_in_milk = np.random.randint(10, 301, n_samples)

    # ambient_temp_C: من 5 إلى 35 درجة
    ambient_temp_C = np.random.uniform(5, 35, n_samples)

    # humidity_pct: من 30% إلى 90%
    humidity_pct = np.random.uniform(30, 90, n_samples)

    # body_condition_score: من 2.0 إلى 4.0
    body_condition_score = np.random.uniform(2.0, 4.0, n_samples)

    # somatic_cell_count: من 50 ألف إلى 800 ألف
    somatic_cell_count = np.random.uniform(50_000, 800_000, n_samples)

    # الآن نعرّف دالة تقريبية لحساب إنتاج الحليب (هدف صناعي)
    # هذا مجرد نموذج مصطنع لغرض التدريب
    # كلما زادت كمية العلف وجودته واعتدلت الحرارة والرطوبة كانت الإنتاجية أعلى
    base = 15
    milk_yield_L = (
        base
        + 0.8 * feed_intake_kg
        + 3.0 * feed_quality_score
        + 1.5 * (parity == 2)
        + 2.5 * (parity == 3)
        - 0.03 * np.abs(days_in_milk - 120)  # أعلى إنتاج حول اليوم 120
        - 0.1 * np.maximum(0, ambient_temp_C - 25)  # الحرارة العالية تقلل الإنتاج
        - 0.03 * np.maximum(0, humidity_pct - 70)   # الرطوبة العالية تقلل
        + 1.0 * (body_condition_score - 3)
        - 0.00001 * somatic_cell_count
    )

    # إضافة ضوضاء عشوائية
    noise = np.random.normal(0, 2, n_samples)
    milk_yield_L = milk_yield_L + noise

    data = pd.DataFrame({
        "feed_intake_kg": feed_intake_kg,
        "feed_quality_score": feed_quality_score,
        "parity": parity,
        "days_in_milk": days_in_milk,
        "ambient_temp_C": ambient_temp_C,
        "humidity_pct": humidity_pct,
        "body_condition_score": body_condition_score,
        "somatic_cell_count": somatic_cell_count,
        "milk_yield_L": milk_yield_L
    })

    return data

def train_and_save_model():
    # 1) توليد/جمع البيانات
    df = generate_synthetic_data(n_samples=2000)

    # 2) تقسيم البيانات لميزات (X) وهدف (y)
    feature_cols = [
        "feed_intake_kg",
        "feed_quality_score",
        "parity",
        "days_in_milk",
        "ambient_temp_C",
        "humidity_pct",
        "body_condition_score",
        "somatic_cell_count"
    ]

    X = df[feature_cols]
    y = df["milk_yield_L"]

    # 3) train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4) إنشاء نموذج الانحدار الخطي وتدريبه
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5) التقييم
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Model evaluation:")
    print(f"MSE: {mse:.2f}")
    print(f"R2:  {r2:.3f}")

    # 6) حفظ النموذج
    joblib.dump(model, "milk_model.joblib")
    print("Model saved as milk_model.joblib")

if __name__ == "__main__":
    train_and_save_model()
