"""
Configuration settings for EcoFreonTrack
Supports multiple environments (development, production, testing)
"""
import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).parent


class Config:
    """Base configuration - common settings across all environments"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Supabase settings
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    USE_SUPABASE = os.environ.get('DATABASE_TYPE', 'sqlite').lower() == 'supabase'

    # Application settings
    APP_NAME = 'EcoFreonTrack'
    APP_VERSION = '1.0.0'

    # EPA 608 Compliance settings
    DEFAULT_LEAK_THRESHOLD_COMMERCIAL = 10.0  # 10% for commercial refrigeration
    DEFAULT_LEAK_THRESHOLD_COMFORT = 20.0     # 20% for comfort cooling
    DEFAULT_LEAK_THRESHOLD_SMALL = 30.0       # 30% for appliances < 50 lbs
    DEFAULT_INSPECTION_FREQUENCY = 30         # days

    # Alert settings
    CERTIFICATION_EXPIRY_WARNING_DAYS = 30    # Warn 30 days before cert expires
    LOW_INVENTORY_WARNING = True


class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    TESTING = False

    # Use development database - Supabase or SQLite
    if Config.USE_SUPABASE:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DB_URL')
        if not SQLALCHEMY_DATABASE_URI:
            raise ValueError("SUPABASE_DB_URL must be set when DATABASE_TYPE=supabase")
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            f'sqlite:///{BASE_DIR}/instance/epa608_tracker_dev.db'

    # Development-specific settings
    SQLALCHEMY_ECHO = True  # Log all SQL queries (helpful for debugging)


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False

    # Use production database - Supabase or SQLite
    if Config.USE_SUPABASE:
        SQLALCHEMY_DATABASE_URI = os.environ.get('SUPABASE_DB_URL')
        if not SQLALCHEMY_DATABASE_URI:
            raise ValueError("SUPABASE_DB_URL must be set when DATABASE_TYPE=supabase")
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            f'sqlite:///{BASE_DIR}/instance/epa608_tracker_prod.db'

    # Production security
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production!

    # Production-specific settings
    SQLALCHEMY_ECHO = False  # Don't log SQL queries in production

    # Enable additional security measures
    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing environment configuration"""

    DEBUG = True
    TESTING = True

    # Use separate test database
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/instance/epa608_tracker_test.db'

    # Testing-specific settings
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration based on environment

    Args:
        env: Environment name ('development', 'production', 'testing')
             If None, uses FLASK_ENV environment variable or defaults to 'development'

    Returns:
        Configuration class for the specified environment
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')

    return config.get(env, config['default'])
