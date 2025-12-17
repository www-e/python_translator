from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from utils.logger import setup_logger
import os

logger = setup_logger(__name__)

class ArabicPDFGenerator:
    """Generate PDF with proper Arabic text rendering"""
    
    def __init__(self, output_path):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.margin = 50
        self.line_height = 20
        self.font_size = 12
        self.font_name = "Amiri"
        self._setup_arabic_font()
        
    def _setup_arabic_font(self):
        """Register Arabic font from local file or Windows fonts"""
        try:
            # Try project fonts folder first
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            fonts_dir = os.path.join(project_root, 'fonts')
            font_path = os.path.join(fonts_dir, 'Amiri-Regular.ttf')
            
            if os.path.exists(font_path):
                logger.info(f"Using Arabic font from: {font_path}")
                pdfmetrics.registerFont(TTFont(self.font_name, font_path))
                logger.info("Arabic font registered successfully")
                return
            
            # Try Windows fonts as fallback
            windows_fonts = [
                "C:/Windows/Fonts/tahoma.ttf",
                "C:/Windows/Fonts/tahomabd.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/arialbd.ttf",
            ]
            
            for win_font in windows_fonts:
                if os.path.exists(win_font):
                    logger.info(f"Using Windows font: {win_font}")
                    pdfmetrics.registerFont(TTFont(self.font_name, win_font))
                    logger.info("Windows Arabic font registered successfully")
                    return
            
            raise Exception("No Arabic font found. Please add Amiri-Regular.ttf to fonts/ folder")
            
        except Exception as e:
            logger.error(f"Failed to setup Arabic font: {str(e)}")
            raise
    
    def _prepare_arabic_text(self, text):
        """Reshape and reorder Arabic text for proper RTL display"""
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    
    def generate_pdf(self, translated_pages, progress_callback=None):
        """Generate PDF with Arabic text"""
        logger.info(f"Generating Arabic PDF: {self.output_path}")
        
        try:
            c = canvas.Canvas(self.output_path, pagesize=A4)
            total_pages = len(translated_pages)
            
            for i, page_data in enumerate(translated_pages):
                self._add_page(c, page_data['text'], page_data['page'])
                
                if progress_callback:
                    progress_callback(i + 1, total_pages)
            
            c.save()
            logger.info(f"PDF generated successfully: {self.output_path}")
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise
    
    def _add_page(self, canvas_obj, text, page_number):
        """Add a single page with selectable Arabic text"""
        canvas_obj.setFont(self.font_name, self.font_size)
        
        # Prepare text for RTL rendering
        prepared_text = self._prepare_arabic_text(text)
        
        # Starting position (top-right for RTL)
        x = self.page_width - self.margin
        y = self.page_height - self.margin
        
        # Maximum width for text
        max_width = self.page_width - (2 * self.margin)
        
        # Split into lines
        lines = prepared_text.split('\n')
        
        for line in lines:
            if not line.strip():
                y -= self.line_height  # Empty line
                continue
            
            # Simple word wrapping
            words = line.split(' ')
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                text_width = canvas_obj.stringWidth(test_line, self.font_name, self.font_size)
                
                if text_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        # Draw the line
                        if y < self.margin + 50:
                            canvas_obj.showPage()
                            canvas_obj.setFont(self.font_name, self.font_size)
                            y = self.page_height - self.margin
                        
                        canvas_obj.drawRightString(x, y, ' '.join(current_line))
                        y -= self.line_height
                    current_line = [word]
            
            # Draw remaining words
            if current_line:
                if y < self.margin + 50:
                    canvas_obj.showPage()
                    canvas_obj.setFont(self.font_name, self.font_size)
                    y = self.page_height - self.margin
                
                canvas_obj.drawRightString(x, y, ' '.join(current_line))
                y -= self.line_height
        
        # Add page number
        canvas_obj.setFont(self.font_name, 10)
        canvas_obj.drawCentredString(self.page_width / 2, 30, f"صفحة {page_number}")
        
        canvas_obj.showPage()
