import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from config import WINDOW_TITLE, WINDOW_SIZE, THEME_COLOR
from core.pdf_extractor import PDFExtractor
from core.translator import OfflineTranslator
from core.pdf_generator import ArabicPDFGenerator
from utils.validators import validate_pdf_file, validate_output_path, ValidationError
from utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFTranslatorApp:
    """Main GUI application for PDF translation"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)
        
        # Translator instance
        self.translator = None
        
        self._build_ui()
        
    def _build_ui(self):
        """Build the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="English to Arabic PDF Translator",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file section
        ttk.Label(main_frame, text="Input PDF (English):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.input_file, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5
        )
        ttk.Button(main_frame, text="Browse", command=self._browse_input).grid(
            row=1, column=2, pady=5
        )
        
        # Output file section
        ttk.Label(main_frame, text="Output PDF (Arabic):").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5
        )
        ttk.Button(main_frame, text="Browse", command=self._browse_output).grid(
            row=2, column=2, pady=5
        )
        
        # Translate button
        self.translate_btn = ttk.Button(
            main_frame,
            text="Translate PDF",
            command=self._start_translation,
            style="Accent.TButton"
        )
        self.translate_btn.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Status label
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=("Arial", 10)
        )
        status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Log text area
        ttk.Label(main_frame, text="Process Log:").grid(
            row=6, column=0, columnspan=3, sticky=tk.W, pady=(10, 5)
        )
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(7, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def _browse_input(self):
        """Browse for input PDF file"""
        filename = filedialog.askopenfilename(
            title="Select English PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-set output filename
            base_name = os.path.splitext(filename)[0]
            self.output_file.set(f"{base_name}_arabic.pdf")
    
    def _browse_output(self):
        """Browse for output PDF location"""
        filename = filedialog.asksaveasfilename(
            title="Save Arabic PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def _log(self, message):
        """Add message to log text area"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def _update_progress(self, current, total):
        """Update progress bar"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def _start_translation(self):
        """Start translation process in separate thread"""
        # Validate inputs
        try:
            validate_pdf_file(self.input_file.get())
            validate_output_path(self.output_file.get())
        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
            return
        
        # Disable button during processing
        self.translate_btn.configure(state='disabled')
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        
        # Run translation in separate thread
        thread = threading.Thread(target=self._translate_pdf, daemon=True)
        thread.start()
    
    def _translate_pdf(self):
        """Perform PDF translation (runs in separate thread)"""
        try:
            self.status_text.set("Extracting text from PDF...")
            self._log("Starting PDF extraction...")
            
            # Extract text
            extractor = PDFExtractor(self.input_file.get())
            pages_content = extractor.extract_text()
            self._log(f"Extracted {len(pages_content)} pages")
            self._update_progress(1, 3)
            
            # Initialize translator if needed
            if not self.translator:
                self.status_text.set("Initializing offline translator...")
                self._log("Initializing translator (first-time may download models)...")
                self.translator = OfflineTranslator()
                self._log("Translator ready")
            
            # Translate
            self.status_text.set("Translating to Arabic...")
            self._log("Translating pages...")
            
            def translation_progress(current, total):
                self._log(f"Translated page {current}/{total}")
            
            translated_pages = self.translator.translate_pages(
                pages_content,
                progress_callback=translation_progress
            )
            self._update_progress(2, 3)
            
            # Generate PDF
            self.status_text.set("Generating Arabic PDF...")
            self._log("Generating Arabic PDF...")
            
            generator = ArabicPDFGenerator(self.output_file.get())
            generator.generate_pdf(translated_pages)
            self._update_progress(3, 3)
            
            # Success
            self.status_text.set("Translation completed successfully!")
            self._log(f"✓ Translation complete: {self.output_file.get()}")
            messagebox.showinfo("Success", f"PDF translated successfully!\n\nSaved to:\n{self.output_file.get()}")
            
        except Exception as e:
            self.status_text.set("Translation failed")
            self._log(f"✗ Error: {str(e)}")
            logger.error(f"Translation failed: {str(e)}", exc_info=True)
            messagebox.showerror("Translation Error", f"An error occurred:\n{str(e)}")
        
        finally:
            # Re-enable button
            self.translate_btn.configure(state='normal')
    
    def run(self):
        """Start the application"""
        logger.info("Starting GUI application")
        self.root.mainloop()
