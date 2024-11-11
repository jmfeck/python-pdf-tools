# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import warnings
from ebooklib import ITEM_DOCUMENT, epub
from fpdf import FPDF
from bs4 import BeautifulSoup  # to clean HTML content for text extraction
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "EPUB to PDF Converter"

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)

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

logging.info("Starting EPUB to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for EPUB files in the input folder...")

# List and count EPUB files
input_epub_files = [f for f in os.listdir(path_input) if f.endswith(".epub")]
input_num_epubs = len(input_epub_files)
logging.info(f"Found {input_num_epubs} EPUB file(s) to process.")

# Check if there are any EPUB files to process
if not input_epub_files:
    logging.warning("No EPUB files found in the input folder. Exiting the program.")
    sys.exit()

# Process each EPUB file
for epub_file in input_epub_files:
    epub_path = os.path.join(path_input, epub_file)
    logging.info(f"Processing file: {epub_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        
        # Load EPUB file
        book = epub.read_epub(epub_path)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Extract text from EPUB and add to PDF
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                # Decode the HTML content, parse with BeautifulSoup, and extract plain text
                content = item.get_body_content().decode('utf-8')
                soup = BeautifulSoup(content, "html.parser")
                text_content = soup.get_text()

                # Add page and content to PDF
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, text_content)

        # Save the PDF
        output_filename = f"{timestamp}_{epub_file.split('.')[0]}.pdf"
        output_path = os.path.join(path_output, output_filename)
        pdf.output(output_path)
        logging.info(f"Converted {epub_file} to PDF at {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {epub_file} - {e}")

logging.info("EPUB to PDF Conversion Process Completed Successfully")
logging.info(f"Total EPUB files processed: {input_num_epubs}")
