import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Used for session management and CSRF protection
    DEBUG = False  # Disable debug mode by default
    TESTING = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Folder to store uploaded files
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max file size for uploads (16MB)

    # Supported file extensions for uploads
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'xml', 'musicxml'}

    # Tesseract configuration (for handling image-based sheet music)
    TESSERACT_CMD = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')

    # Application-specific configurations (if needed)
    SHEET_MUSIC_PROCESSING_TIMEOUT = 300  # Timeout for processing sheet music (in seconds)

    # Logging configuration (optional)
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'logs/app.log'
    LOGGING_LEVEL = 'DEBUG'

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True  # Enable debug mode for development
    ENV = 'development'

class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True  # Enable testing mode
    DEBUG = True  # Still want debug information during tests
    ENV = 'testing'

class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False  # Disable debug mode for production
    ENV = 'production'

# Dictionary to map different configuration environments
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env):
    """Retrieve configuration based on the current environment."""
    return config.get(env, Config)

