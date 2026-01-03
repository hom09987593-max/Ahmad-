import axios from "axios";

const API_URL = "http://127.0.0.1:8000/"; // تغييرها عند النشر

export const predictMilkYield = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, data);
    return response.data;
  } catch (error) {
    console.error("Error predicting milk yield:", error);
    throw error;
  }
};

export const getDashboardData = async () => {
  try {
    const response = await axios.get(`${API_URL}/dashboard`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};
