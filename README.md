# Fake_review_detection
ake reviews create unfair competition, manipulate product ratings, and negatively impact both consumers and businesses. Manually verifying large volumes of reviews is impractical, which makes automated solutions essential.  This project was developed to:  Improve trust in online review systems .

📌 Overview

Online reviews significantly influence consumer decisions, but fake and spam reviews reduce trust and fairness.
This project implements a Machine Learning–based Fake Review Detection System that classifies textual reviews as REAL or FAKE using Natural Language Processing (NLP) techniques.

The system supports both single review prediction and batch review analysis using CSV files through a simple web interface.

🎯 Objectives

Detect fake or misleading reviews automatically

Apply NLP techniques to preprocess textual data

Train and evaluate multiple supervised ML models

Build an end-to-end ML pipeline with a web interface

🧠 Approach

Collect and preprocess review text

Clean text using NLP techniques (tokenization, stopword removal, lemmatization)

Convert text into numerical features using TF-IDF

Train and evaluate multiple ML models

Select the best-performing model

Deploy the model using a Flask-based web application

✨ Features

Classifies reviews as REAL or FAKE

NLP preprocessing pipeline

Feature extraction using TF-IDF and sentiment analysis

Model comparison and evaluation

Web-based interface using Flask

CSV batch processing support

🛠️ Tech Stack

Programming Language: Python

Machine Learning: Scikit-learn

Natural Language Processing: NLTK, TextBlob

Web Framework: Flask

Data Handling: Pandas, NumPy

Frontend: HTML, CSS, Bootstrap
