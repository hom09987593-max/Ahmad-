import { useState } from "react";
import axios from "axios";

function App() {
  const [result, setResult] = useState(null);

  const predictMilkYield = async () => {
    const data = {
      feedintakekg: 12.5,
      feedqualityscore: 0.9,
      parity: 2,
      daysinmilk: 120,
      ambienttempC: 25.0,
      humidity_pct: 60.0,
      bodyconditionscore: 3.5,
      somaticcellcount: 200
    };

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", data);
      setResult(res.data.milk_yield_L);
    } catch (err) {
      console.error("Error calling API:", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-blue-600">Milk Yield Prediction</h1>
      <button 
        onClick={predictMilkYield} 
        className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Predict
      </button>
      {result && <p className="mt-4 text-lg">Predicted Yield: {result} L</p>}
    </div>
  );
}

export default App;