import axios from 'axios';
import { RiskScoreResponse, TextAnalysisResponse, VisualAnalysisResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

export interface ReturnCase {
  case_id: string;
  user_id: string;
  customer_id: string;
  abuse_type: string;
  description: string;
  status: string;
  reported_at: string;
  refund_method_type: string;
  action_taken: string;
  return_reason: string;
  risk_score: number;
  suspicion_score: number;
  product_category: string;
  timestamp: string;
}

export interface ReturnCaseStatistics {
  total_cases: number;
  avg_risk_score: number;
  avg_suspicion_score: number;
  high_risk_cases: number;
  medium_risk_cases: number;
  low_risk_cases: number;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const returnCaseApi = {
  // Get all return cases with pagination and filters
  getReturnCases: async (params: {
    page?: number;
    per_page?: number;
    min_score?: number;
    max_score?: number;
    product_category?: string;
    action_taken?: string;
  }) => {
    // Remove empty string filters before sending the request
    const filteredParams = { ...params };
    if (!filteredParams.product_category) delete filteredParams.product_category;
    if (!filteredParams.action_taken) delete filteredParams.action_taken;
    const response = await api.get('/get-return-cases', { params: filteredParams });
    return response.data;
  },

  // Get a single return case by ID
  getReturnCase: async (id: string) => {
    const response = await api.get(`/get-return-case/${id}`);
    return response.data;
  },

  // Save a new return case
  saveReturnCase: async (data: Omit<ReturnCase, 'timestamp'>) => {
    const response = await api.post('/save-return-case', data);
    return response.data;
  },

  // Update a return case
  updateReturnCase: async (id: string, data: Partial<ReturnCase>) => {
    const response = await api.put(`/update-return-case/${id}`, data);
    return response.data;
  },

  // Delete a return case
  deleteReturnCase: async (id: string) => {
    const response = await api.delete(`/delete-return-case/${id}`);
    return response.data;
  },

  // Get return case statistics
  getStatistics: async () => {
    const response = await api.get('/return-case-statistics');
    return response.data;
  },
};

export const predictRiskScore = async (data: {
    return_frequency: number;
    average_return_time: number;
    product_category_diversity: number;
    reason_diversity_score: number;
    refund_method_type: string;
    prior_fraud_similarity_score: number;
}): Promise<RiskScoreResponse> => {
    const response = await api.post('/predict-score', data);
    return response.data;
};

export const analyzeReturnReason = async (returnReason: string): Promise<TextAnalysisResponse> => {
    const response = await api.post('/analyze-text', { return_reason: returnReason });
    return response.data;
};

export const detectVisualMismatch = async (
    originalImage: File,
    returnedImage: File
): Promise<VisualAnalysisResponse> => {
    const formData = new FormData();
    formData.append('original_image', originalImage);
    formData.append('returned_image', returnedImage);

    const response = await api.post('/detect-visual-mismatch', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
}; 