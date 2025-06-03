import spacy
import re
from transformers import pipeline
from typing import Dict, List

class ReturnReasonAnalyzer:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Load sentiment analyzer
        self.sentiment_analyzer = pipeline("sentiment-analysis")

        # Define suspicious patterns
        self.suspicious_patterns = [
            "not as expected", "item broken", "defective", "not working",
            "wrong item", "damaged", "poor quality", "not what i ordered",
            "doesn't fit", "too small", "too large"
        ]

        # Define scripted phrases
        self.scripted_phrases = [
            "as described", "exactly as", "perfect condition",
            "brand new", "never used", "still in box", "original packaging"
        ]

        # Scoring weights
        self.weights = {
            'pattern': 0.2,
            'scripted': 0.15,
            'length': 0.1,
            'sentiment': 0.2
        }

    def analyze_text(self, return_reason: str) -> Dict:
        text_lower = return_reason.lower()

        # Match suspicious patterns
        pattern_matches = [
            pattern for pattern in self.suspicious_patterns
            if re.search(r'\b' + re.escape(pattern) + r'\b', text_lower)
        ]

        # Match scripted phrases
        scripted_matches = [
            phrase for phrase in self.scripted_phrases
            if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower)
        ]

        # Sentiment analysis
        sentiment_result = self.sentiment_analyzer(return_reason)[0]
        sentiment_score = sentiment_result['score']
        sentiment_label = sentiment_result['label']

        # Adjust sentiment weight based on label
        if sentiment_label == 'NEGATIVE':
            sentiment_penalty = sentiment_score * self.weights['sentiment']
        elif sentiment_label == 'POSITIVE':
            sentiment_penalty = (1 - sentiment_score) * self.weights['sentiment']
        else:
            sentiment_penalty = 0.05

        # Word count
        doc = self.nlp(return_reason)
        word_count = len([token for token in doc if not token.is_punct])

        # Score calculation
        pattern_score = len(pattern_matches) * self.weights['pattern']
        scripted_score = len(scripted_matches) * self.weights['scripted']
        length_score = min(word_count / 50, 1.0) * self.weights['length']

        suspicion_score = min(pattern_score + scripted_score + length_score + sentiment_penalty, 1.0)

        # Reason summary
        reasons = []
        if pattern_matches:
            reasons.append("suspicious phrases detected")
        if scripted_matches:
            reasons.append("scripted/boilerplate language detected")
        if sentiment_label == 'NEGATIVE':
            reasons.append("negative sentiment")
        if word_count < 10:
            reasons.append("very short explanation")

        return {
            'suspicion_score': round(suspicion_score, 3),
            'pattern_matches': pattern_matches,
            'scripted_phrases': scripted_matches,
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'word_count': word_count,
            'reason_summary': ", ".join(reasons) if reasons else "no strong indicators"
        }

    def batch_analyze(self, return_reasons: List[str]) -> List[Dict]:
        # Batch sentiment analysis
        sentiment_results = self.sentiment_analyzer(return_reasons)
        return [
            self.analyze_text(reason) for reason in return_reasons
        ]

# Example usage
if __name__ == "__main__":
    analyzer = ReturnReasonAnalyzer()
    test_reasons = [
        "The item was not as expected and arrived damaged. It's not working properly.",
        "The product is exactly as described but doesn't fit me well.",
        "Item is still in box, never used, perfect condition. Just not what I ordered.",
        "The quality is poor and the item is defective. It's not working at all."
    ]

    for reason in test_reasons:
        result = analyzer.analyze_text(reason)
        print(f"\nReturn Reason: {reason}")
        print(json.dumps(result, indent=2))
