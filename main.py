import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.main_window import PDFTranslatorApp
from utils.logger import setup_logger

def main():
    """Main application entry point"""
    # Setup logging
    logger = setup_logger()
    logger.info("Starting PDF Translator Application")
    
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('temp', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Launch GUI
    app = PDFTranslatorApp()
    app.run()

if __name__ == "__main__":
    main()
