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
import pdfkit
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "HTML to PDF Converter"

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

logging.info("Starting HTML to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for HTML files in the input folder...")

# List and count HTML files
input_html_files = [f for f in os.listdir(path_input) if f.endswith(".html")]
input_num_htmls = len(input_html_files)
logging.info(f"Found {input_num_htmls} HTML file(s) to process.")

# Check if there are any HTML files to process
if not input_html_files:
    logging.warning("No HTML files found in the input folder. Exiting the program.")
    sys.exit()

# Process each HTML file
for html_file in input_html_files:
    html_path = os.path.join(path_input, html_file)
    logging.info(f"Processing file: {html_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        
        # Define the output PDF file path
        output_filename = f"{timestamp}_{html_file.split('.')[0]}.pdf"
        output_path = os.path.join(path_output, output_filename)

        # Convert HTML to PDF
        pdfkit.from_file(html_path, output_path)
        logging.info(f"Converted {html_file} to PDF at {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {html_file} - {e}")

logging.info("HTML to PDF Conversion Process Completed Successfully")
logging.info(f"Total HTML files processed: {input_num_htmls}")