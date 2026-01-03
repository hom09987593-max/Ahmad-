import React, { useState } from "react";

const InputForm = ({ onPredict }) => {
  const [formData, setFormData] = useState({
    feed_intake_kg: "",
    feed_quality_score: "",
    parity: "",
    days_in_milk: "",
    ambient_temp_C: "",
    humidity_pct: "",
    body_condition_score: "",
    somatic_cell_count: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onPredict(formData);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-xl shadow-md border-t-4 border-blue-600">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-right">
        إدخال البيانات الفنية للإنتاج
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4 text-right" dir="rtl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* كمية العلف */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              كمية العلف (كجم)
            </label>
            <input
              type="number"
              name="feed_intake_kg"
              value={formData.feed_intake_kg}
              onChange={handleChange}
              step="0.01"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* جودة العلف - تم التعديل هنا */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              جودة العلف (من 0 إلى 1)
            </label>
            <input
              type="number"
              name="feed_quality_score"
              value={formData.feed_quality_score}
              onChange={handleChange}
              step="0.01" // للسماح بأرقام مثل 0.55
              min="0"
              max="1"
              placeholder="مثال: 0.85"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 border-blue-500 outline-none transition bg-blue-50"
              required
            />
          </div>

          {/* عدد الولادات */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              عدد الولادات (Parity)
            </label>
            <input
              type="number"
              name="parity"
              value={formData.parity}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* أيام إدرار الحليب */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              أيام الإدرار (Days in Milk)
            </label>
            <input
              type="number"
              name="days_in_milk"
              value={formData.days_in_milk}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* درجة الحرارة */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              درجة الحرارة (C°)
            </label>
            <input
              type="number"
              name="ambient_temp_C"
              value={formData.ambient_temp_C}
              onChange={handleChange}
              step="0.1"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* الرطوبة */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              الرطوبة (%)
            </label>
            <input
              type="number"
              name="humidity_pct"
              value={formData.humidity_pct}
              onChange={handleChange}
              min="0"
              max="100"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* حالة الجسم */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              حالة الجسم (1-5)
            </label>
            <input
              type="number"
              name="body_condition_score"
              value={formData.body_condition_score}
              onChange={handleChange}
              step="0.1"
              max="5"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>

          {/* عدد الخلايا الصمغية */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              خلايا SCC
            </label>
            <input
              type="number"
              name="somatic_cell_count"
              value={formData.somatic_cell_count}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition"
              required
            />
          </div>
        </div>

        <div className="flex justify-center pt-6">
          <button
            type="submit"
            className="px-12 py-4 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition duration-300 shadow-xl transform hover:scale-105"
          >
            تحليل وتوقع الإنتاج 📊
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputForm;
