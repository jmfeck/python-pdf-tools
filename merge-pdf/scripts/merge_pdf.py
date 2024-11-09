# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import argparse
import logging
from PyPDF2 import PdfMerger
from datetime import datetime

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

# Set up logging
os.makedirs(path_log_folder, exist_ok=True)
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[
                        logging.FileHandler(path_log),
                        logging.StreamHandler(sys.stdout)
                    ])

# Argument parser setup
parser = argparse.ArgumentParser(description="Merge PDF files by filename or creation date.")
parser.add_argument("--sort", choices=["filename", "date"], default="filename", 
                    help="Sort order for merging: 'filename' or 'date'")
args = parser.parse_args()

logging.info("PDF Merger: Starting")
logging.info("PDF Merger: Searching for PDF files to merge in the input folder...")

# List and sort PDF files based on the argument
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
input_num_pdfs = len(input_pdf_files)
logging.info(f"PDF Merger: {input_num_pdfs} PDF(s) found")

# Check if there are any PDF files to process
if not input_pdf_files:
    logging.info("PDF Merger: No PDF files found. Exiting the program.")
    sys.exit()

#sorting merge order
if args.sort == "filename":
    input_pdf_files.sort()  # Sort by filename
    logging.info("PDF Merger: Sorting by filename")
elif args.sort == "date":
    input_pdf_files.sort(key=lambda f: os.path.getctime(os.path.join(path_input, f)))  # Sort by creation date
    logging.info("PDF Merger: Sorting by creation date")

# Initialize PdfMerger and start merging files
merger = PdfMerger()
logging.info("PDF Merger: Merging files...")
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    logging.info(f"PDF Merger: Merging {pdf_file}")
    merger.append(pdf_path)

# Generate a timestamped filename for the output PDF
output_filename = f"{timestamp}_merged_pdf.pdf"
output_path = os.path.join(path_output, output_filename)

# Ensure the output folder exists and save the merged file
os.makedirs(path_output, exist_ok=True)
logging.info(f"PDF Merger: Exporting merged PDF to {output_path}")
merger.write(output_path)
merger.close()

logging.info("PDF Merger: Process completed successfully.")
