#!/usr/bin/env python3
"""
Setup script for Fake Review Detection System
"""

from setuptools import setup, find_packages

setup(
    name='fake-review-detector',
    version='1.0.0',
    description='AI-powered fake review detection system',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.3',
        'scikit-learn==1.3.0',
        'pandas==2.0.3',
        'numpy==1.24.3',
        'textblob==0.17.1',
        'joblib==1.3.2',
        'scipy==1.11.1',
        'nltk==3.8.1',
        'gunicorn==21.2.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
