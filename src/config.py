import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Translation settings
SOURCE_LANG = 'en'
TARGET_LANG = 'ar'

# PDF Processing
MAX_PDF_SIZE_MB = 50
SUPPORTED_FORMATS = ['.pdf']

# Performance settings
BATCH_SIZE = 100  # Process text in batches
MAX_WORKERS = 4   # Parallel processing workers

# GUI settings
WINDOW_TITLE = "PDF English to Arabic Translator"
WINDOW_SIZE = "800x600"
THEME_COLOR = "#2c3e50"
