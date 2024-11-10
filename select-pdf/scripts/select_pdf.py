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
PROGRAM_NAME = "PDF Page Selector"

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
parser = argparse.ArgumentParser(description="Select specific pages from PDF files and save them individually.")
parser.add_argument("--pages", type=str, required=True,
                    help="Page ranges to select, e.g., '1-3,5,7-9'.")
args = parser.parse_args()

logging.info("Starting PDF Page Selection Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Page ranges: {args.pages}")
logging.info("Searching for PDF files in the input folder...")

# Parse page ranges
def parse_page_ranges(page_ranges):
    ranges = []
    for part in page_ranges.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ranges.append((start - 1, end - 1))  # Convert to 0-based index
        else:
            page_num = int(part) - 1  # Convert to 0-based index
            ranges.append((page_num, page_num))
    return ranges

page_ranges = parse_page_ranges(args.pages)

# List and count PDF files
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
input_num_pdfs = len(input_pdf_files)
logging.info(f"Found {input_num_pdfs} PDF file(s) to process.")

# Check if there are any PDF files to process
if not input_pdf_files:
    logging.warning("No PDF files found in the input folder. Exiting.")
    sys.exit()

# Process each PDF file individually
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        doc = fitz.open(pdf_path)
        selected_doc = fitz.open()  # Empty document for selected pages

        # Add specified pages to the individual selected document
        for start_page, end_page in page_ranges:
            if start_page < len(doc) and end_page < len(doc):
                selected_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
                logging.info(f"  - Added pages {start_page + 1}-{end_page + 1} from {pdf_file}")
            else:
                logging.warning(f"  - Page range {start_page + 1}-{end_page + 1} is out of range for {pdf_file}")

        # Save the selected pages as a new PDF
        if len(selected_doc) > 0:
            output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_selected_pages.pdf"
            output_path = os.path.join(path_output, output_filename)
            selected_doc.save(output_path)
            selected_doc.close()
            logging.info(f"Selected pages saved to {output_filename}")
        else:
            logging.warning(f"No pages were added to the output for {pdf_file}.")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Page Selection Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
