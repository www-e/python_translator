from googletrans import Translator
from utils.logger import setup_logger
import time

logger = setup_logger(__name__)

class OfflineTranslator:
    """Fast translation using Google Translate (no API key needed)"""
    
    def __init__(self):
        self.translator = Translator()
        logger.info("Translator initialized")
    
    def translate_text(self, text, progress_callback=None):
        """Translate text preserving structure"""
        if not text or not text.strip():
            return ""
        
        logger.info(f"Translating text of length: {len(text)}")
        
        try:
            # Split into chunks (Google Translate has 5000 char limit per request)
            chunks = []
            lines = text.split('\n')
            current_chunk = []
            current_length = 0
            
            for line in lines:
                line_length = len(line)
                if current_length + line_length > 4500 and current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = [line]
                    current_length = line_length
                else:
                    current_chunk.append(line)
                    current_length += line_length + 1
            
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            
            # Translate chunks
            translated_chunks = []
            total = len(chunks)
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():
                    result = self.translator.translate(chunk, src='en', dest='ar')
                    translated_chunks.append(result.text)
                else:
                    translated_chunks.append('')
                
                if progress_callback:
                    progress_callback(i + 1, total)
                
                time.sleep(0.1)  # Small delay to avoid rate limiting
            
            final_result = '\n'.join(translated_chunks)
            logger.info("Translation completed successfully")
            return final_result
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    def translate_pages(self, pages_content, progress_callback=None):
        """Translate multiple pages with progress tracking"""
        translated_pages = []
        total_pages = len(pages_content)
        
        for i, page_data in enumerate(pages_content):
            logger.info(f"Translating page {page_data['page']}/{total_pages}")
            
            translated_text = self.translate_text(page_data['text'])
            translated_pages.append({
                'page': page_data['page'],
                'text': translated_text
            })
            
            if progress_callback:
                progress_callback(i + 1, total_pages)
        
        return translated_pages
