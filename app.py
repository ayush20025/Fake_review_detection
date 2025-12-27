"""
Fake Review Detection System
A comprehensive web application for detecting fake product reviews using machine learning.
Author: AI Assistant
Date: September 2025
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import joblib
import pandas as pd
import numpy as np
from textblob import TextBlob
import os
import json
import logging
from datetime import datetime
from scipy.sparse import hstack
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

# Load models and preprocessing components
MODEL_DIR = 'models'

try:
    model = joblib.load(os.path.join(MODEL_DIR, 'best_model.pkl'))
    tfidf_vectorizer = joblib.load(os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl'))
    feature_scaler = joblib.load(os.path.join(MODEL_DIR, 'feature_scaler.pkl'))
    metadata = joblib.load(os.path.join(MODEL_DIR, 'model_metadata.pkl'))
except Exception as e:
    print("Model loading error:", e)

    logger.info("Models loaded successfully!")
    logger.info(f"Model: {metadata['model_name']}")
    logger.info(f"Accuracy: {metadata['accuracy']:.4f}")

except Exception as e:
    logger.error(f"Error loading models: {e}")
    model = None
    tfidf_vectorizer = None
    feature_scaler = None
    metadata = None

def extract_features(text):
    """Extract additional features from review text"""
    features = {}

    # Basic text features
    features['length'] = len(text)
    features['word_count'] = len(text.split())
    features['avg_word_length'] = np.mean([len(word) for word in text.split()])
    features['sentence_count'] = len(text.split('.'))

    # Punctuation features
    features['exclamation_count'] = text.count('!')
    features['question_count'] = text.count('?')
    features['capital_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0

    # Sentiment analysis
    try:
        blob = TextBlob(text)
        features['polarity'] = blob.sentiment.polarity
        features['subjectivity'] = blob.sentiment.subjectivity
    except:
        features['polarity'] = 0
        features['subjectivity'] = 0

    # Repetitive words (common in fake reviews)
    words = text.lower().split()
    unique_words = set(words)
    features['unique_word_ratio'] = len(unique_words) / len(words) if len(words) > 0 else 0

    return features

def predict_review(review_text):
    """Predict if a review is fake or real"""
    if not model or not tfidf_vectorizer or not feature_scaler:
        return {"error": "Models not loaded properly"}

    try:
        # Extract text features
        text_features = tfidf_vectorizer.transform([review_text])

        # Extract numerical features
        numerical_features = extract_features(review_text)
        feature_array = np.array([[numerical_features[col] for col in metadata['feature_names']]])
        scaled_features = feature_scaler.transform(feature_array)

        # Combine features
        combined_features = hstack([text_features, scaled_features])

        # Make prediction
        prediction = model.predict(combined_features)[0]
        prediction_proba = model.predict_proba(combined_features)[0]

        # Get confidence scores
        fake_confidence = prediction_proba[0] if model.classes_[0] == 'fake' else prediction_proba[1]
        real_confidence = prediction_proba[1] if model.classes_[1] == 'real' else prediction_proba[0]

        return {
            "prediction": prediction,
            "fake_confidence": float(fake_confidence),
            "real_confidence": float(real_confidence),
            "features": numerical_features,
            "success": True
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"error": str(e), "success": False}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', metadata=metadata)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/how_it_works')
def how_it_works():
    """How it works page"""
    return render_template('how_it_works.html')

@app.route('/dataset')
def dataset():
    """Dataset information page"""
    try:
        # Load dataset info
        df = pd.read_csv(os.path.join(MODEL_DIR, 'fake_review_dataset.csv'))
        dataset_info = {
            'total_reviews': len(df),
            'fake_reviews': len(df[df['label'] == 'fake']),
            'real_reviews': len(df[df['label'] == 'real']),
            'avg_rating': df['rating'].mean(),
            'verified_purchase_ratio': df['verified_purchase'].mean()
        }
        return render_template('dataset.html', dataset_info=dataset_info)
    except Exception as e:
        logger.error(f"Error loading dataset info: {e}")
        return render_template('dataset.html', dataset_info=None)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        review_text = data.get('review_text', '').strip()

        if not review_text:
            return jsonify({"error": "No review text provided", "success": False})

        result = predict_review(review_text)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Prediction endpoint error: {e}")
        return jsonify({"error": str(e), "success": False})

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """Batch prediction endpoint"""
    try:
        if 'file' not in request.files:
            flash('No file uploaded')
            return redirect(url_for('index'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))

        if file and file.filename.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(file)

            if 'review_text' not in df.columns:
                flash('CSV file must contain a "review_text" column')
                return redirect(url_for('index'))

            results = []
            for idx, row in df.iterrows():
                review_text = str(row['review_text'])
                prediction_result = predict_review(review_text)

                if prediction_result.get('success'):
                    results.append({
                        'review_text': review_text,
                        'prediction': prediction_result['prediction'],
                        'fake_confidence': prediction_result['fake_confidence'],
                        'real_confidence': prediction_result['real_confidence']
                    })

            return render_template('batch_results.html', results=results)
        else:
            flash('Please upload a CSV file')
            return redirect(url_for('index'))

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/stats')
def api_stats():
    """API statistics endpoint"""
    try:
        return jsonify({
            "model_name": metadata['model_name'] if metadata else "Unknown",
            "accuracy": metadata['accuracy'] if metadata else 0,
            "features_count": len(metadata['feature_names']) if metadata else 0,
            "status": "online"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
