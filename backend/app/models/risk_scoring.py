import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import joblib
import os


class ReturnRiskScoringEngine:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_columns = [
            'return_frequency',
            'average_return_time',
            'product_category_diversity',
            'reason_diversity_score',
            'refund_method_type',
            'prior_fraud_similarity_score'
        ]

    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic customer data with labeled risk scores."""
        np.random.seed(42)
        data = {
            'return_frequency': np.random.uniform(0, 20, n_samples),
            'average_return_time': np.random.uniform(1, 90, n_samples),
            'product_category_diversity': np.random.uniform(1, 10, n_samples),
            'reason_diversity_score': np.random.uniform(0, 1, n_samples),
            'refund_method_type': np.random.choice(
                ['credit_card', 'store_credit', 'gift_card', 'cash'], n_samples
            ),
            'prior_fraud_similarity_score': np.random.uniform(0, 1, n_samples)
        }

        # Calculate risk score with weighted logic
        risk_score = (
            data['return_frequency'] * 2 +
            (90 - data['average_return_time']) * 0.5 +
            data['product_category_diversity'] * 3 +
            data['reason_diversity_score'] * 20 +
            (data['refund_method_type'] == 'cash').astype(int) * 10 +
            data['prior_fraud_similarity_score'] * 30
        )

        # Normalize to 0–100
        risk_score = (risk_score - risk_score.min()) / (risk_score.max() - risk_score.min()) * 100
        data['return_risk_score'] = risk_score
        return pd.DataFrame(data)

    def prepare_preprocessor(self):
        """Create feature transformer for numerical and categorical fields."""
        numeric_features = [
            'return_frequency',
            'average_return_time',
            'product_category_diversity',
            'reason_diversity_score',
            'prior_fraud_similarity_score'
        ]
        categorical_features = ['refund_method_type']

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )
        return preprocessor

    def train(self, data=None):
        """Train the XGBoost model pipeline with preprocessing."""
        if data is None:
            data = self.generate_synthetic_data()

        X = data[self.feature_columns]
        y = data['return_risk_score']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.preprocessor = self.prepare_preprocessor()

        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

        pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('model', model)
        ])

        pipeline.fit(X_train, y_train)
        self.model = pipeline

        print(f"Training R² score: {pipeline.score(X_train, y_train):.3f}")
        print(f"Testing R² score: {pipeline.score(X_test, y_test):.3f}")
        return pipeline

    def predict(self, customer_data):
        """Predict risk score from a customer data dict or DataFrame."""
        if self.model is None:
            raise ValueError("Model not trained. Please call train() first.")

        if isinstance(customer_data, dict):
            customer_data = pd.DataFrame([customer_data])

        # Validate required columns
        missing_cols = set(self.feature_columns) - set(customer_data.columns)
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        return float(self.model.predict(customer_data)[0])

    def save_model(self, path='models/risk_scoring_model.joblib'):
        """Save the trained pipeline model to disk."""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")

    def load_model(self, path='models/risk_scoring_model.joblib'):
        """Load a trained pipeline model from disk."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found at: {path}")
        self.model = joblib.load(path)
        print(f"Model loaded from {path}")


# --- Example Usage ---
if __name__ == "__main__":
    engine = ReturnRiskScoringEngine()
    engine.train()

    sample_customer = {
        'return_frequency': 5,
        'average_return_time': 30,
        'product_category_diversity': 3,
        'reason_diversity_score': 0.5,
        'refund_method_type': 'credit_card',
        'prior_fraud_similarity_score': 0.2
    }

    score = engine.predict(sample_customer)
    print(f"Predicted Return Risk Score: {score:.2f}")
