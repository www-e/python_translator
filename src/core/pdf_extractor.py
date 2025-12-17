import pdfplumber
from PyPDF2 import PdfReader
from utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFExtractor:
    """Extract text from PDF files with RTL support"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text_content = []
        
    def extract_text(self):
        """Extract text from PDF using pdfplumber for better Arabic support"""
        logger.info(f"Extracting text from: {self.pdf_path}")
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"Total pages: {total_pages}")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text with left-to-right direction for English
                    text = page.extract_text()
                    
                    if text:
                        self.text_content.append({
                            'page': page_num,
                            'text': text.strip()
                        })
                        logger.debug(f"Extracted page {page_num}/{total_pages}")
                    else:
                        logger.warning(f"No text found on page {page_num}")
                
                logger.info(f"Successfully extracted text from {len(self.text_content)} pages")
                return self.text_content
                
        except Exception as e:
            logger.error(f"Failed to extract text: {str(e)}")
            raise
    
    def get_full_text(self):
        """Get all extracted text as single string"""
        if not self.text_content:
            self.extract_text()
        return '\n\n'.join([page['text'] for page in self.text_content])
