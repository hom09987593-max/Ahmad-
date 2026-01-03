import React, { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";
import InputForm from "./components/InputForm";
import Results from "./components/Results";
import axios from "axios";

function App() {
  const [status, setStatus] = useState("جاري الاتصال بالسيرفر...");
  const [currentPage, setCurrentPage] = useState("input");
  const [prediction, setPrediction] = useState(null);
  const [features, setFeatures] = useState(null);

  const BACKEND_URL = "http://localhost:8000";

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/`)
      .then((response) => {
        setStatus("متصل: " + response.data.message);
      })
      .catch((error) => {
        console.error("خطأ في الاتصال:", error);
        setStatus("فشل الاتصال بالـ Backend. تأكد من تشغيل السيرفر.");
      });
  }, []);

  const handlePredict = async (formData) => {
    try {
      setStatus("جاري تحليل البيانات...");

      const response = await axios.post(`${BACKEND_URL}/predict`, {
        feed_intake_kg: parseFloat(formData.feed_intake_kg) || 0,
        feed_quality_score: parseFloat(formData.feed_quality_score) || 0,
        parity: parseInt(formData.parity) || 0,
        days_in_milk: parseInt(formData.days_in_milk) || 0,
        ambient_temp_C: parseFloat(formData.ambient_temp_C) || 0,
        humidity_pct: parseFloat(formData.humidity_pct) || 0,
        body_condition_score: parseFloat(formData.body_condition_score) || 0,
        somatic_cell_count: parseInt(formData.somatic_cell_count) || 0,
      });

      setPrediction(response.data.prediction.toFixed(2));
      setFeatures(formData);
      setCurrentPage("results");
      setStatus("متصل");
    } catch (error) {
      console.error("خطأ في التوقع:", error);
      alert("حدث خطأ أثناء الاتصال بالـ Backend");
      setStatus("فشل الاتصال");
    }
  };

  const pages = {
    input: <InputForm onPredict={handlePredict} />,
    results: (
      <Results
        prediction={prediction}
        features={features}
        onBack={() => setCurrentPage("input")}
      />
    ),
    dashboard: <Dashboard onBack={() => setCurrentPage("input")} />,
  };

  return (
    <div
      className="min-h-screen bg-gradient-to-b from-blue-50 to-gray-100 text-right"
      dir="rtl"
    >
      <nav className="bg-white shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-blue-800">
              🐄 نظام توقع إنتاج الحليب اليومي
            </h1>

            <div className="flex space-x-4 space-x-reverse">
              <button
                className={`px-4 py-2 rounded-lg transition ${
                  currentPage === "input"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700"
                }`}
                onClick={() => setCurrentPage("input")}
              >
                إدخال البيانات
              </button>

              <button
                className={`px-4 py-2 rounded-lg transition ${
                  currentPage === "dashboard"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700"
                }`}
                onClick={() => setCurrentPage("dashboard")}
              >
                لوحة المتابعة
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div
        className={`text-center py-1 text-sm ${
          status.includes("فشل")
            ? "bg-red-100 text-red-700"
            : "bg-green-100 text-green-700"
        }`}
      >
        {status}
      </div>

      <main className="container mx-auto px-4 py-8">{pages[currentPage]}</main>

      <footer className="bg-white border-t mt-8 py-4 text-center text-gray-600">
        <p>نظام توقع إنتاج الحليب - مشروع 13 | © 2024</p>
      </footer>
    </div>
  );
}

export default App;
