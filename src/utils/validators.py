import os
from config import MAX_PDF_SIZE_MB, SUPPORTED_FORMATS

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_pdf_file(file_path):
    """Validate PDF file exists and is within size limits"""
    if not os.path.exists(file_path):
        raise ValidationError(f"File does not exist: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValidationError(f"Path is not a file: {file_path}")
    
    # Check extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in SUPPORTED_FORMATS:
        raise ValidationError(f"Unsupported format: {ext}. Supported: {SUPPORTED_FORMATS}")
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_PDF_SIZE_MB:
        raise ValidationError(f"File too large: {file_size_mb:.2f}MB. Max: {MAX_PDF_SIZE_MB}MB")
    
    return True

def validate_output_path(output_path):
    """Validate output directory is writable"""
    output_dir = os.path.dirname(output_path)
    
    if not output_dir:
        output_dir = os.getcwd()
    
    if not os.path.exists(output_dir):
        raise ValidationError(f"Output directory does not exist: {output_dir}")
    
    if not os.access(output_dir, os.W_OK):
        raise ValidationError(f"Output directory is not writable: {output_dir}")
    
    return True
