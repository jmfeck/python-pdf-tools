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

# Timestamp for file and log naming
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

# Set up logging with both file and console output
os.makedirs(path_log_folder, exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
file_handler = logging.FileHandler(path_log)
logging.getLogger().addHandler(file_handler)

# Argument parser setup
parser = argparse.ArgumentParser(description="Compress PDF files.")
parser.add_argument("--img-quality", type=int, default=None,
                    help="Quality level for image recompression (1-100). Omit to skip image compression.")
parser.add_argument("--compression-level", type=int, default=5, choices=range(1, 10),
                    help="Deflate compression level for content streams (1-9). Default: 5.")
args = parser.parse_args()

logging.info("PDF Compressor: Starting")
logging.info("PDF Compressor: Searching for PDF files to compress in the input folder...")

# List PDF files in the input folder
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
input_num_pdfs = len(input_pdf_files)
logging.info(f"PDF Compressor: {input_num_pdfs} PDF(s) found")

# Check if there are any PDF files to process
if not input_pdf_files:
    logging.info("PDF Compressor: No PDF files found. Exiting the program.")
    sys.exit()

# Compress each PDF file
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    compressed_output_filename = f"{timestamp}_compressed_{pdf_file}"
    compressed_output_path = os.path.join(path_output, compressed_output_filename)

    logging.info(f"PDF Compressor: Compressing {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        lz.read(pdf_path).compress(img_quality=args.img_quality, compression_level=args.compression_level).to_pdf(compressed_output_path)
        logging.info(f"PDF Compressor: Compressed PDF saved to {compressed_output_path}")
    except Exception as e:
        logging.error(f"PDF Compressor: Failed to compress {pdf_file} - {e}")

logging.info("PDF Compressor: Process completed successfully.")
