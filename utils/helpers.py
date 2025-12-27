"""
Utility functions for the Fake Review Detection System
"""

import re
import pandas as pd
import numpy as np
from textblob import TextBlob
import joblib
import os

def clean_text(text):
    """Clean and normalize text for processing"""
    if not isinstance(text, str):
        return ""

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s\.\!\?\,\:\;\-'"]', '', text)

    return text

def extract_advanced_features(text):
    """Extract advanced features from review text"""
    features = {}

    if not text:
        return {f: 0 for f in ['length', 'word_count', 'avg_word_length', 
                              'sentence_count', 'exclamation_count', 'question_count',
                              'capital_ratio', 'polarity', 'subjectivity', 'unique_word_ratio']}

    # Basic text statistics
    features['length'] = len(text)
    words = text.split()
    features['word_count'] = len(words)
    features['avg_word_length'] = np.mean([len(word) for word in words]) if words else 0
    features['sentence_count'] = len(re.split(r'[.!?]+', text))

    # Punctuation analysis
    features['exclamation_count'] = text.count('!')
    features['question_count'] = text.count('?')
    features['capital_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0

    # Sentiment analysis
    try:
        blob = TextBlob(text)
        features['polarity'] = blob.sentiment.polarity
        features['subjectivity'] = blob.sentiment.subjectivity
    except:
        features['polarity'] = 0
        features['subjectivity'] = 0

    # Vocabulary richness
    if words:
        unique_words = set(word.lower() for word in words)
        features['unique_word_ratio'] = len(unique_words) / len(words)
    else:
        features['unique_word_ratio'] = 0

    # Additional features for fake review detection
    features['avg_sentence_length'] = features['word_count'] / max(features['sentence_count'], 1)
    features['punctuation_ratio'] = sum(1 for c in text if c in '!?.,;:') / len(text) if text else 0

    # Check for suspicious patterns
    suspicious_words = ['amazing', 'perfect', 'excellent', 'terrible', 'worst', 'best ever', 'highly recommend']
    features['suspicious_word_count'] = sum(1 for word in suspicious_words if word.lower() in text.lower())

    return features

def validate_csv_format(file_path):
    """Validate CSV file format for batch processing"""
    try:
        df = pd.read_csv(file_path)

        if 'review_text' not in df.columns:
            return False, "CSV must contain 'review_text' column"

        if len(df) == 0:
            return False, "CSV file is empty"

        if len(df) > 1000:
            return False, "CSV file too large (max 1000 reviews)"

        return True, "Valid CSV format"

    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"

def load_model_components(model_dir='models'):
    """Load all model components"""
    try:
        model = joblib.load(os.path.join(model_dir, 'best_model.pkl'))
        tfidf = joblib.load(os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'feature_scaler.pkl'))
        metadata = joblib.load(os.path.join(model_dir, 'model_metadata.pkl'))

        return model, tfidf, scaler, metadata
    except Exception as e:
        raise Exception(f"Error loading model components: {str(e)}")

def calculate_confidence_level(prediction_proba):
    """Calculate confidence level based on prediction probabilities"""
    max_proba = max(prediction_proba)

    if max_proba >= 0.9:
        return "Very High"
    elif max_proba >= 0.8:
        return "High"
    elif max_proba >= 0.7:
        return "Medium"
    elif max_proba >= 0.6:
        return "Low"
    else:
        return "Very Low"

def format_prediction_result(prediction, probabilities, features):
    """Format prediction result for display"""
    fake_prob = probabilities[0] if hasattr(probabilities, '__len__') else 0
    real_prob = probabilities[1] if hasattr(probabilities, '__len__') and len(probabilities) > 1 else 1 - fake_prob

    result = {
        'prediction': prediction,
        'fake_confidence': float(fake_prob),
        'real_confidence': float(real_prob),
        'confidence_level': calculate_confidence_level(probabilities),
        'features': features,
        'risk_level': 'High' if prediction == 'fake' and fake_prob > 0.8 else 'Medium' if fake_prob > 0.6 else 'Low'
    }

    return result

def generate_explanation(prediction, features):
    """Generate human-readable explanation for the prediction"""
    explanations = []

    if prediction == 'fake':
        if features.get('exclamation_count', 0) > 3:
            explanations.append("Excessive use of exclamation marks")

        if features.get('capital_ratio', 0) > 0.1:
            explanations.append("High ratio of capital letters")

        if features.get('unique_word_ratio', 1) < 0.5:
            explanations.append("Low vocabulary diversity (repetitive words)")

        if abs(features.get('polarity', 0)) > 0.8:
            explanations.append("Extremely polarized sentiment")

        if features.get('word_count', 0) < 20:
            explanations.append("Very short review length")

    else:  # real
        if features.get('unique_word_ratio', 0) > 0.7:
            explanations.append("Good vocabulary diversity")

        if 50 <= features.get('word_count', 0) <= 200:
            explanations.append("Appropriate review length")

        if 0.2 <= abs(features.get('polarity', 0)) <= 0.6:
            explanations.append("Balanced sentiment expression")

    return explanations if explanations else ["Based on overall text patterns and features"]
