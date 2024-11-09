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
import pandas as pd
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Table Extractor with PyMuPDF"

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
logging.basicConfig(level=logging.INFO, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

# Argument parser setup
parser = argparse.ArgumentParser(description="Extract tables from PDF files and save in CSV or Excel format.")
parser.add_argument("--export-format", type=str, choices=["csv", "excel"], default="csv",
                    help="Output format for the extracted tables: 'csv' or 'excel' (default: csv)")
args = parser.parse_args()

logging.info("Starting PDF Table Extraction Process with PyMuPDF")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Output format: {args.export_format}")
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
        doc = fitz.open(pdf_path)  # Open the PDF document with PyMuPDF
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            logging.info(f"Processing page {page_num + 1}")
            
            # Extract text blocks (can approximate table structure)
            blocks = page.get_text("blocks")
            table_data = []

            for block in blocks:
                if len(block) >= 5:  # Ensure block has enough values
                    text = block[4]  # Text content
                    if text.strip():  # Skip empty blocks
                        rows = text.splitlines()
                        table_data.append(rows)

            # Only proceed if we have valid table data meeting the minimum size requirement
            if table_data:
                output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_page{page_num + 1}"
                
                # Save table data as CSV or Excel
                if args.export_format == "csv":
                    output_path = os.path.join(path_output, f"{output_filename}.csv")
                    pd.DataFrame(table_data).to_csv(output_path, index=False, header=False)
                    logging.info(f"Table on page {page_num + 1} saved as CSV: {output_path}")
                elif args.export_format == "excel":
                    output_path = os.path.join(path_output, f"{output_filename}.xlsx")
                    pd.DataFrame(table_data).to_excel(output_path, index=False, header=False)
                    logging.info(f"Table on page {page_num + 1} saved as Excel: {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Table Extraction Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
