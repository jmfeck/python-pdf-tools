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
from datetime import datetime
from pypdf import PdfWriter

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
#console_handler = logging.StreamHandler(sys.stdout)
logging.getLogger().addHandler(file_handler)
#logging.getLogger().addHandler(console_handler)

# Argument parser setup
parser = argparse.ArgumentParser(description="Compress PDF files and optionally set image quality.")
parser.add_argument("--img-quality", type=int, choices=range(1, 100),
                    help="Set the quality level for image compression (0-100). If not provided, image compression is skipped.")
parser.add_argument("--compression-level", type=int, choices=range(1, 10), default=5,
                    help="Set the compression level for content streams (1-9). Default is 5.")
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

    if args.img_quality is not None:
        logging.info(f"PDF Compressor: Compressing {pdf_file} with image quality {args.img_quality}")
    else:
        logging.info(f"PDF Compressor: Compressing {pdf_file} without image quality adjustment")
    logging.info(f"PDF Compressor: Using compression level {args.compression_level} for content streams")

    try:
        os.makedirs(path_output, exist_ok=True)
        writer = PdfWriter(clone_from=pdf_path)
        
        writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        
        for page in writer.pages:
            if args.img_quality is not None:
                for img in page.images:
                    img.replace(img.image, quality=args.img_quality)

            page.compress_content_streams(level=args.compression_level)

        with open(compressed_output_path, "wb") as f:
            writer.write(f)
        
        logging.info(f"PDF Compressor: Compressed PDF saved to {compressed_output_path}")
    except Exception as e:
        logging.error(f"PDF Compressor: Failed to compress {pdf_file} - {e}")

logging.info("PDF Compressor: Process completed successfully.")