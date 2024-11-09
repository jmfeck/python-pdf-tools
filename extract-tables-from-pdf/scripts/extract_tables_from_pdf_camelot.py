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
import camelot
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Table Extractor"

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
parser.add_argument("--flavor", type=str, choices=["stream", "lattice"], default="lattice",
                    help="Table extraction method: 'lattice' for tables with borders, 'stream' for tables without (default: lattice)")
args = parser.parse_args()

logging.info("Starting PDF Table Extraction Process with Camelot")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Output format: {args.export_format}")
logging.info(f"Extraction flavor: {args.flavor}")
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
        
        # Extract tables with camelot
        tables = camelot.read_pdf(pdf_path, flavor=args.flavor, pages="all")
        
        if tables:
            for table_index, table in enumerate(tables, start=1):
                try:
                    page_number = table.page
                    output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_page{page_number}_table{table_index}"                
                    if args.export_format == "csv":
                        output_path = os.path.join(path_output, f"{output_filename}.csv")
                        table.to_csv(output_path, index=False)
                        logging.info(f"Table {table_index} saved as CSV: {output_filename}.csv")
                    elif args.export_format == "excel":
                        output_path = os.path.join(path_output, f"{output_filename}.xlsx")
                        table.to_excel(output_path, index=False)
                        logging.info(f"Table {table_index} saved as Excel: {output_filename}.xlsx")
                except Exception as e:
                    logging.error(f"Failed to save table {table_index} - {e}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Table Extraction Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
