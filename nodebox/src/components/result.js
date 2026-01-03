import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Results = ({ prediction, features, onBack }) => {
  // تجهيز تسميات عربية للخصائص
  const labelsMap = {
    feed_intake_kg: "كمية العلف",
    feed_quality_score: "جودة العلف",
    parity: "عدد الولادات",
    days_in_milk: "أيام الإدرار",
    ambient_temp_C: "درجة الحرارة",
    humidity_pct: "الرطوبة",
    body_condition_score: "حالة الجسم",
    somatic_cell_count: "عدد الخلايا",
  };

  // تجهيز بيانات الرسم
  const chartData = {
    labels: Object.keys(features || {}).map((key) => labelsMap[key] || key),
    datasets: [
      {
        label: "قيمة المتغير",
        data: Object.values(features || {}),
        backgroundColor: [
          "#3B82F6",
          "#10B981",
          "#F59E0B",
          "#EF4444",
          "#8B5CF6",
          "#EC4899",
          "#14B8A6",
          "#F97316",
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  // توصيات ذكية
  const recommendations = [
    {
      condition: features?.feed_quality_score < 0.6,
      text: "🔄 يُفضل تحسين جودة العلف لرفع الإنتاج",
    },
    {
      condition: features?.ambient_temp_C > 30,
      text: "🌡️ درجة الحرارة مرتفعة — حاول توفير تبريد للحظيرة",
    },
    {
      condition: features?.somatic_cell_count > 200,
      text: "⚠️ مستوى SCC مرتفع — ينصح بمراجعة الطبيب البيطري",
    },
    {
      condition: features?.body_condition_score < 2.5,
      text: "📊 حالة الجسم ضعيفة — حسّن التغذية",
    },
  ].filter((rec) => rec.condition);

  return (
    <div className="max-w-6xl mx-auto" dir="rtl">
      {/* ====== الجزء القديم (العرض البسيط) ====== */}
      <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg border-t-4 border-green-500 text-right mb-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          نتائج التوقع الذكي
        </h2>

        <div className="bg-green-50 p-6 rounded-lg text-center mb-8">
          <p className="text-gray-600 mb-2 font-medium">
            كمية الحليب المتوقعة لليوم:
          </p>
          <div className="text-5xl font-black text-green-600">
            {prediction} <span className="text-2xl text-green-700">لتر</span>
          </div>
        </div>

        <div className="space-y-3 mb-8">
          <h3 className="font-bold text-gray-700 border-b pb-2">
            ملخص المدخلات:
          </h3>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <p>
              <span className="text-gray-500">جودة العلف:</span>{" "}
              {features?.feed_quality_score}
            </p>
            <p>
              <span className="text-gray-500">عدد الولادات:</span>{" "}
              {features?.parity}
            </p>
            <p>
              <span className="text-gray-500">أيام الإدرار:</span>{" "}
              {features?.days_in_milk}
            </p>
          </div>
        </div>
      </div>

      {/* ====== الجزء المتطور (الرسم + التوصيات) ====== */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* الرسم البياني */}
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-4 text-gray-800">
              📊 تأثير العوامل على الإنتاج
            </h3>
            <div className="h-80">
              <Bar data={chartData} options={chartOptions} />
            </div>
          </div>

          {/* التوصيات */}
          <div className="bg-blue-50 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-4 text-gray-800">
              💡 توصيات لزيادة الإنتاج
            </h3>

            {recommendations.length > 0 ? (
              <ul className="space-y-4">
                {recommendations.map((rec, index) => (
                  <li key={index} className="p-4 bg-white rounded-lg shadow">
                    {rec.text}
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center p-8">
                <div className="text-6xl mb-4">🎉</div>
                <p className="text-xl text-gray-700">
                  كل المؤشرات ممتازة والإنتاج في المستوى المثالي!
                </p>
              </div>
            )}

            <div className="mt-8 p-4 bg-yellow-50 rounded-lg">
              <h4 className="font-bold text-lg mb-2">📈 ملاحظات:</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                <li>جودة العلف الأعلى تزيد الإنتاج</li>
                <li>درجة الحرارة المثالية 15° – 25°</li>
                <li>انخفاض SCC يعني صحة وإنتاج أفضل</li>
              </ul>
            </div>
          </div>
        </div>

        {/* الأزرار */}
        <div className="flex justify-center mt-8 space-x-4 space-x-reverse">
          <button
            onClick={onBack}
            className="px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-black transition"
          >
            ↩️ العودة للإدخال
          </button>

          <button
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            onClick={() => window.print()}
          >
            🖨️ طباعة التقرير
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;
