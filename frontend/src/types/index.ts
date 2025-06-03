export interface ReturnCase {
  id: string;
  customerId: string;
  productId: string;
  returnReason: string;
  riskScore: number;
  suspicionScore: number;
  visualSimilarity: number;
  status: string;
  timestamp: string;
  productCategory: string;
}

export interface RiskScoreResponse {
  risk_score: number;
  timestamp: string;
}

export interface TextAnalysisResponse {
  suspicion_score: number;
  pattern_matches: string[];
  scripted_phrases: string[];
  sentiment_score: number;
  word_count: number;
  timestamp: string;
}

export interface VisualAnalysisResponse {
  overall_similarity: number;
  ssim_score: number;
  histogram_similarity: number;
  feature_similarity: number;
  is_suspicious: boolean;
  timestamp: string;
} 