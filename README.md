# Fake Review Detection System

A comprehensive web application for detecting fake product reviews using advanced machine learning techniques.

## Features

- **AI-Powered Detection**: Uses Random Forest classifier with TF-IDF vectorization and custom features
- **Real-time Analysis**: Instant prediction of review authenticity
- **Batch Processing**: Upload CSV files for bulk analysis
- **Interactive UI**: Modern, responsive web interface
- **Detailed Analytics**: Confidence scores and feature analysis
- **Multiple Pages**: Home, About, How It Works, Dataset information

## Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, pandas, numpy
- **NLP**: TextBlob, NLTK
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn ready

## Installation

1. Clone or extract the project:
   ```bash
   cd fake_review_detector
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('vader_lexicon')
   ```

## Usage

1. **Development Mode**:
   ```bash
   python app.py
   ```
   Access the application at `http://localhost:5000`

2. **Production Mode**:
   ```bash
   gunicorn app:app
   ```

## Project Structure

```
fake_review_detector/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── models/               # ML models and data
│   ├── best_model.pkl    # Trained classifier
│   ├── tfidf_vectorizer.pkl
│   ├── feature_scaler.pkl
│   └── *.csv             # Dataset files
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── how_it_works.html
│   ├── dataset.html
│   └── batch_results.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
└── utils/                # Utility functions
```

## Features Analyzed

### Text Features
- Review length and word count
- Average word length
- Sentence structure
- Punctuation patterns
- Capital letter usage

### Sentiment Analysis
- Emotional polarity (positive/negative)
- Subjectivity levels
- Sentiment consistency

### Behavioral Indicators
- Word uniqueness ratio
- Repetitive phrases
- Generic expressions
- Spam indicators

## API Endpoints

- `GET /` - Main page
- `GET /about` - About page
- `GET /how_it_works` - How it works page
- `GET /dataset` - Dataset information
- `POST /predict` - Single review prediction
- `POST /batch_predict` - Batch file upload
- `GET /api/stats` - System statistics

## Model Performance

The system uses a Random Forest classifier trained on a balanced dataset of fake and authentic reviews, achieving high accuracy in distinguishing between genuine and deceptive content.

## Contributing

This is a final year academic project showcasing machine learning applications in natural language processing and web development.

## License

This project is for educational purposes as part of a final year project.

## Contact

For questions or suggestions regarding this project, please refer to the About page in the application.
