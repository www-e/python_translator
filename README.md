# PDF English to Arabic Translator

Offline PDF translation application with GUI interface that translates English PDFs to Arabic using open-source libraries.

## Features

- ✅ Offline translation (no internet required after setup)
- ✅ Simple GUI interface
- ✅ High-performance processing
- ✅ Proper Arabic RTL text handling
- ✅ Critical data security (local processing only)
- ✅ Progress tracking
- ✅ Comprehensive logging

## Installation

1. **Create virtual environment:**
python -m venv venv


2. **Activate virtual environment:**
- Windows: `.\venv\Scripts\activate`

3. **Install dependencies:**
pip install -r requirements.txt


4. **First run downloads translation models (~200MB)**

## Usage

Run the application:
python main.py
1. Click "Browse" to select input English PDF
2. Choose output location for Arabic PDF
3. Click "Translate PDF"
4. Wait for processing to complete

## Requirements

- Python 3.8+
- 500MB free disk space (for models)
- 2GB RAM minimum

## Project Structure

- `src/core/` - Core translation and PDF processing logic
- `src/gui/` - Tkinter GUI interface
- `src/utils/` - Utilities and validators
- `models/` - Translation model storage
- `temp/` - Temporary processing files
- `logs/` - Application logs

## License

MIT License