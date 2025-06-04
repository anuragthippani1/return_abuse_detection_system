import axios from "axios";

const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:5001/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const returnCaseApi = {
  getReturnCases: async (params) => {
    const filteredParams = { ...params, limit: 100 };
    if (!filteredParams.product_category)
      delete filteredParams.product_category;
    if (!filteredParams.action_taken) delete filteredParams.action_taken;
    const response = await api.get("/get-return-cases", {
      params: filteredParams,
    });
    return response.data;
  },

  getReturnCase: async (id) => {
    const response = await api.get(`/get-return-case/${id}`);
    return response.data;
  },

  saveReturnCase: async (data) => {
    const response = await api.post("/save-return-case", data);
    return response.data;
  },

  updateReturnCase: async (id, data) => {
    const response = await api.put(`/update-return-case/${id}`, data);
    return response.data;
  },

  deleteReturnCase: async (id) => {
    const response = await api.delete(`/delete-return-case/${id}`);
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get("/return-case-statistics");
    return response.data;
  },
};

export const predictRiskScore = async (data) => {
  const response = await api.post("/predict-score", data);
  return response.data;
};

export const analyzeReturnReason = async (returnReason) => {
  const response = await api.post("/analyze-text", {
    return_reason: returnReason,
  });
  return response.data;
};

export const detectVisualMismatch = async (originalImage, returnedImage) => {
  const formData = new FormData();
  formData.append("original_image", originalImage);
  formData.append("returned_image", returnedImage);

  const response = await api.post("/detect-visual-mismatch", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};
