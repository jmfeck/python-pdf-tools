# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import fitz  # PyMuPDF for flattening PDF content
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Flattener"

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

# Configure root logger for console output
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

logging.info("Starting PDF Flattening Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for PDF files in the input folder...")

# List and count PDF files
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
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
        
        # Open the PDF and create a new document for flattened output
        doc = fitz.open(pdf_path)
        output_pdf_path = os.path.join(path_output, f"{timestamp}_flattened_{pdf_file}")

        # Flatten each page by rendering it and saving the result
        flattened_doc = fitz.open()  # Create a new PDF to save flattened pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Render the page to an image to flatten it
            pix = page.get_pixmap()  # Creates a pixmap image of the page
            flattened_page = flattened_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Insert the rendered image as a single layer
            flattened_page.insert_image(page.rect, pixmap=pix)
            logging.info(f"Flattened page {page_num + 1} of {pdf_file}")

        # Save the flattened PDF
        flattened_doc.save(output_pdf_path)
        flattened_doc.close()
        doc.close()

        logging.info(f"Flattened PDF saved as {output_pdf_path}")

    except Exception as e:
        logging.error(f"Failed to flatten {pdf_file} - {e}")

logging.info("PDF Flattening Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
