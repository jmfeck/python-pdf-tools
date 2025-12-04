# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import fitz  # PyMuPDF
import pytesseract
from datetime import datetime
from PIL import Image

# Program name for log prefix
PROGRAM_NAME = "PDF OCR Text Extractor with PyMuPDF"

# Set up timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folder and file paths
input_foldername = 'input'
output_foldername = 'output'
log_foldername = 'logs'
log_filename = f"{timestamp}_log.log"

# Define paths
path_script = os.path.realpath(__file__)
path_project = os.path.dirname(os.path.dirname(path_script))
path_input = os.path.join(path_project, input_foldername)
path_output = os.path.join(path_project, output_foldername)
path_log_folder = os.path.join(path_project, log_foldername)
path_log = os.path.join(path_log_folder, log_filename)

# Set up logging with program name as prefix in each log entry
os.makedirs(path_log_folder, exist_ok=True)
log_format = f"{PROGRAM_NAME}: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

logging.info("Starting OCR Text Extraction Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for PDF files in the input folder...")

# List and count PDF files
input_pdf_files = [f for f in os.listdir(path_input) if f.lower().endswith(".pdf")]
input_num_pdfs = len(input_pdf_files)
logging.info(f"Found {input_num_pdfs} PDF file(s) to process.")

# Check if there are any PDF files to process
if not input_pdf_files:
    logging.warning("No PDF files found in the input folder. Exiting the program.")
    sys.exit()

# Process each PDF file
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        doc = fitz.open(pdf_path)
        
        # Extract text from each page and perform OCR if necessary
        pdf_text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text("text")

            # If text extraction fails, convert to image and perform OCR
            if not page_text.strip():
                logging.info(f"Page {page_num + 1} appears to be scanned. Attempting OCR.")
                # Render page as an image for OCR
                pix = page.get_pixmap(dpi=150)  # 150 dpi for decent OCR accuracy
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)

            if page_text.strip():  # Only add non-empty text
                pdf_text += f"\n\n--- Page {page_num + 1} ---\n{page_text.strip()}"

        # Skip saving if text is empty
        if pdf_text.strip():
            output_filename = f"{timestamp}_{pdf_file.split('.')[0]}.txt"
            output_path = os.path.join(path_output, output_filename)
            with open(output_path, "w", encoding="utf-8") as text_file:
                text_file.write(pdf_text)
            logging.info(f"Text extracted and saved to {output_filename}")
        else:
            logging.info(f"No text found in {pdf_file}. Skipping export.")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF OCR Text Extraction Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
