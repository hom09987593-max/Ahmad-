#1️⃣ استيراد المكتبات

import pandas as pd
import numpy as np
import os



#2️⃣ إنشاء مجلد البيانات

os.makedirs('data', exist_ok=True)



#3️⃣ تثبيت العشوائية (Seed)

np.random.seed(42)


#4️⃣ تحديد عدد العينات

num_samples = 5000


#5️⃣ توليد البيانات الأساسية (Features)

df = pd.DataFrame({
    'feed_intake_kg': np.random.normal(20, 3, num_samples),
    'feed_quality_score': np.random.uniform(0.5, 1.0, num_samples),
    'parity': np.random.choice(
        [1, 2, 3, 4, 5],
        num_samples,
        p=[0.3, 0.25, 0.2, 0.15, 0.1]
    ),
    'days_in_milk': np.random.randint(1, 300, num_samples),
    'ambient_temp_C': np.random.normal(22, 5, num_samples),
    'humidity_pct': np.random.normal(65, 15, num_samples),
    'body_condition_score': np.random.uniform(2.5, 4.0, num_samples),
    'somatic_cell_count': np.random.lognormal(4.5, 1.2, num_samples)
})



#6️⃣ إنشاء متغير الهدف (إنتاج الحليب)

df['milk_yield'] = (
    25 +
    df['feed_intake_kg'] * 0.8 +
    df['feed_quality_score'] * 15 +

    np.where(df['parity'] == 1, -2,
        np.where(df['parity'] == 2, 1,
            np.where(df['parity'] == 3, 3,
                np.where(df['parity'] == 4, 2, 0)
            )
        )
    ) +

    np.sin(2 * np.pi * df['days_in_milk'] / 300) * 8 +
    -0.2 * (df['ambient_temp_C'] - 22) ** 2 +
    -0.05 * df['humidity_pct'] +
    df['body_condition_score'] * 2 +
    -0.001 * df['somatic_cell_count'] +
    np.random.normal(0, 2, num_samples)
)



#7️⃣ تحديد الحد الأدنى للإنتاج

df['milk_yield'] = df['milk_yield'].clip(lower=5)



#8️⃣ حفظ البيانات في ملف CSV

df.to_csv('data/synthetic_milk_data.csv', index=False)



#9️⃣ عرض معلومات سريعة عن البيانات

print(f"تم توليد {len(df)} عينة بنجاح")
print("إحصاءات البيانات:")
print(df.describe())

