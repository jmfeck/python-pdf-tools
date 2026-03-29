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
import lazypdf as lz
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Splitter"

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
parser = argparse.ArgumentParser(description="Split PDF files into separate files based on specified page ranges.")
parser.add_argument("--pages", type=str, required=True,
                    help="Page ranges to split, e.g., '1-3,5,7-9'. Each page becomes a separate file.")
args = parser.parse_args()

logging.info("Starting PDF Splitting Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Page ranges: {args.pages}")
logging.info("Searching for PDF files in the input folder...")

# Parse page ranges (1-indexed, matching lazypdf convention)
def parse_page_ranges(page_ranges):
    pages = []
    for part in page_ranges.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))

page_numbers = parse_page_ranges(args.pages)

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
        pdf = lz.read(pdf_path)

        for page_num in page_numbers:
            if page_num <= pdf.page_count:
                output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_page_{page_num}.pdf"
                output_path = os.path.join(path_output, output_filename)
                pdf.copy().extract_pages([page_num]).to_pdf(output_path)
                logging.info(f"  - Saved page {page_num} as {output_filename}")
            else:
                logging.warning(f"  - Page {page_num} is out of range for {pdf_file}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Splitting Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
