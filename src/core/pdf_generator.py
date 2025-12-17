from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import arabic_reshaper
from bidi.algorithm import get_display
from utils.logger import setup_logger
from PIL import Image, ImageDraw, ImageFont
import io
import os

logger = setup_logger(__name__)

class ArabicPDFGenerator:
    """Generate PDF with proper Arabic text rendering using PIL"""
    
    def __init__(self, output_path):
        self.output_path = output_path
        self.page_width, self.page_height = A4
        self.margin = 50
        self.line_height = 30
        self.font_size = 20
        
    def _prepare_arabic_text(self, text):
        """Reshape and reorder Arabic text for proper RTL display"""
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    
    def _create_text_image(self, text, width):
        """Create image from Arabic text"""
        prepared_text = self._prepare_arabic_text(text)
        
        # Create a temporary image to measure text
        temp_img = Image.new('RGB', (1, 1), 'white')
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Try to use system Arabic font, fallback to default
        try:
            # Try Windows Arabic font
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", self.font_size)
        except:
            try:
                # Alternative: Segoe UI
                font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", self.font_size)
            except:
                # Last fallback
                font = ImageFont.load_default()
        
        # Split text into lines
        lines = prepared_text.split('\n')
        
        # Calculate image height needed
        total_height = 0
        line_heights = []
        for line in lines:
            if line.strip():
                bbox = temp_draw.textbbox((0, 0), line, font=font)
                line_height = bbox[3] - bbox[1] + 10
            else:
                line_height = self.line_height
            line_heights.append(line_height)
            total_height += line_height
        
        # Create actual image
        img = Image.new('RGB', (int(width), max(int(total_height), 100)), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw text lines (right-aligned for Arabic)
        y_position = 0
        for line, line_height in zip(lines, line_heights):
            if line.strip():
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = width - text_width - 10  # Right align
                draw.text((x_position, y_position), line, font=font, fill='black')
            y_position += line_height
        
        return img
    
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
        """Add a single page with Arabic text as image"""
        # Calculate usable width
        usable_width = self.page_width - (2 * self.margin)
        
        # Create text image
        text_img = self._create_text_image(text, usable_width)
        
        # Convert PIL image to ReportLab ImageReader
        img_buffer = io.BytesIO()
        text_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_reader = ImageReader(img_buffer)
        
        # Calculate position (top of page)
        y_position = self.page_height - self.margin - text_img.height
        
        # If image is too tall, scale it down
        if text_img.height > (self.page_height - 2 * self.margin - 50):
            scale_factor = (self.page_height - 2 * self.margin - 50) / text_img.height
            new_height = text_img.height * scale_factor
            new_width = text_img.width * scale_factor
            canvas_obj.drawImage(img_reader, self.margin, self.margin + 50, 
                               width=new_width, height=new_height)
        else:
            canvas_obj.drawImage(img_reader, self.margin, y_position, 
                               width=text_img.width, height=text_img.height)
        
        # Add page number
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.drawCentredString(self.page_width / 2, 30, f"Page {page_number}")
        
        canvas_obj.showPage()
