import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# 1. قراءة البيانات
df = pd.read_csv("milk_yield_dataset_1000.csv")

# 2. التحقق من الأعمدة المطلوبة
expected_cols = [
    "feed_intake_kg","feed_quality_score","parity","days_in_milk",
    "ambient_temp_C","humidity_pct","body_condition_score",
    "somatic_cell_count","milk_yield_L"
]
missing = [c for c in expected_cols if c not in df.columns]
if missing:
    raise SystemExit(f"Missing columns: {missing}")

# 3. فصل الميزات والهدف
X = df[expected_cols[:-1]]
y = df["milk_yield_L"]

# 4. معالجة بسيطة للبيانات الناقصة إن وُجدت
X = X.fillna(X.mean())
y = y.fillna(y.mean())

# 5. تقسيم البيانات
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. إنشاء وتدريب النموذج
model = LinearRegression()
model.fit(X_train, y_train)

# 7. تقييم النموذج
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.3f}")
print(f"R2:  {r2:.3f}")

# 8. حفظ النموذج
joblib.dump(model, "milk_model_custom.joblib")
print("Saved model to milk_model_custom.joblib")
