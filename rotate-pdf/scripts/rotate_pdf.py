# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import argparse
import fitz  # PyMuPDF
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Rotate Pages"

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

# Argument parser setup
parser = argparse.ArgumentParser(description="Rotate pages of PDF files by 90, 180, or 270 degrees.")
parser.add_argument("--rotate", type=int, choices=[90, 180, 270], default=90,
                    help="Rotation in degrees (90, 180, 270). Default is 90.")
args = parser.parse_args()

rotation_degrees = args.rotate

logging.info("Starting PDF Page Rotation Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Rotation degrees: {rotation_degrees}°")
logging.info("Searching for PDF files in the input folder...")

# List and count PDF files
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
input_num_pdfs = len(input_pdf_files)
logging.info(f"Found {input_num_pdfs} PDF file(s) to process.")

# Check if there are any PDF files to process
if not input_pdf_files:
    logging.warning("No PDF files found in the input folder. Exiting.")
    sys.exit()

# Process each PDF file
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        doc = fitz.open(pdf_path)

        # Rotate each page
        for page_num, page in enumerate(doc, start=1):
            page.set_rotation(rotation_degrees)
            logging.info(f"  - Rotated page {page_num} by {rotation_degrees}°")

        # Save the rotated PDF
        output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_rotated_{rotation_degrees}.pdf"
        output_path = os.path.join(path_output, output_filename)
        doc.save(output_path)
        logging.info(f"Rotated PDF saved to {output_filename}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Page Rotation Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
