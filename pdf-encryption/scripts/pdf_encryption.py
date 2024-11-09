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
from pypdf import PdfReader, PdfWriter
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Encryptor"

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

# Set up logging
os.makedirs(path_log_folder, exist_ok=True)
log_format = f"{PROGRAM_NAME}: %(message)s"

# Configure root logger for console output
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

# Argument parser setup
parser = argparse.ArgumentParser(description="Encrypt PDF files with a password.")
parser.add_argument("--password", type=str, required=True, help="Password to encrypt the output PDF files.")
parser.add_argument("--encryption-algo", type=str, default="AES-256-R5", help="Encryption algorithm (default: AES-256-R5).")
args = parser.parse_args()

logging.info("Starting Process")
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
    logging.info(f"Processing file {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        reader = PdfReader(pdf_path)
        writer = PdfWriter(clone_from=reader)

        # Encrypt the output PDF with the provided password and specified algorithm
        logging.info(f"Encrypting the PDF with password using {args.encryption_algo} algorithm.")
        writer.encrypt(args.password, algorithm=args.encryption_algo)

        # Save the encrypted PDF
        encrypted_output_path = os.path.join(path_output, f"{timestamp}_encrypted_{pdf_file}")
        with open(encrypted_output_path, "wb") as encrypted_file:
            writer.write(encrypted_file)

        logging.info(f"Encrypted PDF saved as {encrypted_output_path}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
