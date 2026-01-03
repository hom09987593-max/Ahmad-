

#1️⃣ تحليل البيانات (EDA – Exploratory Data Analysis)

#الهدف: فهم البيانات قبل بناء النموذج

#فتح ملف synthetic_milk_data.csv

#معرف#ة:ي#م الدنيا والعليا

#العلاقة بين المتغيرات وإنتاج الحليب



#د بسيط (الخطوة التالية مباشرة):

import pandas as pd

df = pd.read_csv('data/synthetic_milk_data.csv')
print(df.head())
print(df.describe())

#📌 هذه الخطوة تثبت أنك فهمت البيانات.


#2️⃣ تقسيم البيانات (Train / Test)

#الهدف: تجهيزها للتعلّم

from sklearn.model_selection import train_test_split

X = df.drop('milk_yield', axis=1)
y = df['milk_yield']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


#3️⃣ تدريب نموذج الانحدار الخطي

#هذا هو قلب المشروع

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)



#4️⃣ تقييم النموذج

from sklearn.metrics import mean_squared_error, r2_score

y_pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

#📌 هنا تثبت أن النظام يتوقع فعليًا.




#5️⃣ (اختياري) حفظ النموذج

import joblib

joblib.dump(model, 'milk_yield_model.pkl')