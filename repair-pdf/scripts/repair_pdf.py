# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
from datetime import datetime
import fitz  # PyMuPDF
import pdfplumber
import pikepdf

# Program name for log prefix
PROGRAM_NAME = "PDF Repair Tool"

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

logging.info("Starting PDF Repair Process")
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
    logging.warning("No PDF files found in the input folder. Exiting.")
    sys.exit()

# Function to attempt repair with PyMuPDF
def repair_with_fitz(pdf_path, output_path):
    try:
        with fitz.open(pdf_path) as doc:
            if doc.page_count > 0:
                doc.save(output_path)
                logging.info(f"Repaired with PyMuPDF and saved to {output_path}")
                return True
    except Exception as e:
        logging.warning(f"PyMuPDF failed to repair: {e}")
    return False

# Function to attempt repair with pdfplumber
def repair_with_pdfplumber(pdf_path, output_path):
    try:
        with pdfplumber.open(pdf_path) as doc:
            if len(doc.pages) > 0:
                pdf_writer = fitz.open()  # Use fitz to create the final output
                for page in doc.pages:
                    pdf_writer.new_page(width=page.width, height=page.height)
                pdf_writer.save(output_path)
                logging.info(f"Repaired with pdfplumber and saved to {output_path}")
                return True
    except Exception as e:
        logging.warning(f"pdfplumber failed to repair: {e}")
    return False

# Function to attempt repair with pikepdf
def repair_with_pikepdf(pdf_path, output_path):
    try:
        with pikepdf.open(pdf_path) as pdf:
            pdf.save(output_path)
            logging.info(f"Repaired with pikepdf and saved to {output_path}")
            return True
    except Exception as e:
        logging.warning(f"pikepdf failed to repair: {e}")
    return False

# Process each PDF file
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_repaired.pdf"
    output_path = os.path.join(path_output, output_filename)
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)

        # Attempt to repair using each method in order of preference
        if repair_with_fitz(pdf_path, output_path):
            continue
        elif repair_with_pdfplumber(pdf_path, output_path):
            continue
        elif repair_with_pikepdf(pdf_path, output_path):
            continue
        else:
            logging.error(f"Failed to repair {pdf_file} - No method succeeded.")
    except Exception as e:
        logging.error(f"Unexpected error for {pdf_file} - {e}")

logging.info("PDF Repair Process Completed")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
