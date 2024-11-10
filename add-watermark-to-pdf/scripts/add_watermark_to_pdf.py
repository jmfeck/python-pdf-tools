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
from PIL import Image

# Program name for log prefix
PROGRAM_NAME = "PDF Background Watermark Adder"

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
parser = argparse.ArgumentParser(description="Add an image watermark to the background of each page in PDF files.")
parser.add_argument("--watermark-path", type=str, required=True, help="Path to the image watermark file.")
parser.add_argument("--watermark-transparency", type=float, default=0.5, help="Transparency level of the watermark (0.0 to 1.0). Default is 0.3.")
args = parser.parse_args()

# Verify watermark file
watermark_path = args.watermark_path
if not os.path.exists(watermark_path):
    logging.error(f"Watermark file not found: {watermark_path}")
    sys.exit()

# Process each PDF in the input folder
input_pdf_files = [f for f in os.listdir(path_input) if f.endswith(".pdf")]
logging.info(f"Found {len(input_pdf_files)} PDF file(s) to process.")

if not input_pdf_files:
    logging.warning("No PDF files found in the input folder. Exiting.")
    sys.exit()

# Open watermark image and apply transparency
try:
    with Image.open(watermark_path) as img:
        img = img.convert("RGBA")
        alpha = int(args.watermark_transparency * 255)  # Scale alpha to 0-255
        img.putalpha(alpha)
        watermark_img_path = "temp_watermark.png"
        img.save(watermark_img_path)
except Exception as e:
    logging.error(f"Failed to process image watermark - {e}")
    sys.exit()

# Apply the watermark as a background
for pdf_file in input_pdf_files:
    pdf_path = os.path.join(path_input, pdf_file)
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        doc = fitz.open(pdf_path)

        # Add watermark as a background to each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            rect = page.rect  # Get page dimensions

            # Place the image watermark as a background
            page.insert_image(rect, filename=watermark_img_path, keep_proportion=True, overlay=False)
            logging.info(f"  - Added watermark to background of page {page_num + 1}")

        # Save the watermarked PDF
        output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_watermarked.pdf"
        output_path = os.path.join(path_output, output_filename)
        doc.save(output_path)
        logging.info(f"Watermarked PDF saved to {output_filename}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

# Cleanup temporary watermark image file
os.remove(watermark_img_path)

logging.info("PDF Background Watermark Addition Process Completed Successfully")
logging.info(f"Total PDF files processed: {len(input_pdf_files)}")
