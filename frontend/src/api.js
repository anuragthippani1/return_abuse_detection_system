import axios from "axios";

const API_BASE_URL = "http://localhost:5001/api";

export const uploadData = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload-data`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || "Error uploading data");
  }
};

export const getReturnCases = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get-return-cases`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.message || "Error fetching return cases"
    );
  }
};
