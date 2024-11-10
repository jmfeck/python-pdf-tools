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
import fitz  # PyMuPDF

# Program name for log prefix
PROGRAM_NAME = "PDF Page Size Adjuster"

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
parser = argparse.ArgumentParser(description="Adjust page size of PDF files.")
parser.add_argument("--size", type=str, choices=["a4", "letter"], default="a4",
                    help="Target page size: 'a4' or 'letter' (default: a4)")
args = parser.parse_args()

# Define standard page sizes
page_sizes = {
    "a4": (595, 842),
    "letter": (612, 792)
}
target_width, target_height = page_sizes[args.size]

logging.info("Starting PDF Page Size Adjustment Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info(f"Target page size: {args.size} ({target_width} x {target_height})")
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
        doc = fitz.open(pdf_path)
        new_doc = fitz.open()  # Create a new document to hold adjusted pages

        # Adjust page size
        for page_num in range(len(doc)):
            page = doc[page_num]
            width, height = page.rect.width, page.rect.height

            # Determine scaling factor while preserving aspect ratio
            scale = min(target_width / width, target_height / height)
            scaled_width = width * scale
            scaled_height = height * scale

            logging.info(f"  - Resizing page {page_num + 1} from {width} x {height} to fit within {target_width} x {target_height}")

            # Create a new blank page with the target dimensions
            new_page = new_doc.new_page(width=target_width, height=target_height)

            # Center the scaled content on the new page
            x_offset = (target_width - scaled_width) / 2
            y_offset = (target_height - scaled_height) / 2

            # Insert the original page on top of the new blank page with scaling and offset
            new_page.show_pdf_page(
                fitz.Rect(x_offset, y_offset, x_offset + scaled_width, y_offset + scaled_height),
                doc, page_num
            )

        # Save the adjusted PDF
        output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_{args.size}.pdf"
        output_path = os.path.join(path_output, output_filename)
        new_doc.save(output_path)
        logging.info(f"Page size adjusted PDF saved to {output_filename}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Page Size Adjustment Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
