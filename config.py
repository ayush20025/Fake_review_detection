"""
Configuration settings for Fake Review Detection System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG') == 'True'

    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'temp_uploads'
    ALLOWED_EXTENSIONS = {'csv', 'txt'}

    # Model settings
    MODEL_DIR = 'models'
    MAX_BATCH_SIZE = 1000
    MIN_REVIEW_LENGTH = 10
    MAX_REVIEW_LENGTH = 5000

    # Performance settings
    CACHE_TIMEOUT = timedelta(hours=1)
    REQUEST_TIMEOUT = 30  # seconds

    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = 'app.log'

    # Rate limiting
    RATE_LIMIT = "100/hour"

    # Analytics
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS') == 'True'
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
