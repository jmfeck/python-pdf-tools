# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
from pypdf import PdfReader
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "PDF Image Extractor"

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

# Configure root logger for console output
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

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
    logging.info(f"Processing file: {pdf_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        reader = PdfReader(pdf_path)
        
        # Process each page and extract images
        for page_num, page in enumerate(reader.pages, start=1):
            images_on_page = list(page.images)
            logging.info(f"Page {page_num}: {len(images_on_page)} image(s) found.")
            
            for img_count, image_file_object in enumerate(images_on_page, start=1):
                img_output_filename = f"{timestamp}_{pdf_file.split('.')[0]}_p{page_num}_{img_count}_{image_file_object.name}"
                img_output_path = os.path.join(path_output, img_output_filename)

                with open(img_output_path, "wb") as fp:
                    fp.write(image_file_object.data)
                
                logging.info(f"  - Extracted image {img_count} from page {page_num} to {img_output_filename}")

    except Exception as e:
        logging.error(f"Failed to process {pdf_file} - {e}")

logging.info("PDF Image Extraction Process Completed Successfully")
logging.info(f"Total PDF files processed: {input_num_pdfs}")
