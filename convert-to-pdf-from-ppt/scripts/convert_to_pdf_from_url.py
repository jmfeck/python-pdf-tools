# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import pdfkit
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "URL to PDF Converter"

# Set up timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Folder and file paths
input_foldername = 'input'
output_foldername = 'output'
log_foldername = 'logs'
input_filename = 'urls.txt'  # File containing the list of URLs
log_filename = f"{timestamp}_log.log"

# Define paths
path_script = os.path.realpath(__file__)
path_project = os.path.dirname(os.path.dirname(path_script))
path_input_folder = os.path.join(path_project, input_foldername)
path_input_file = os.path.join(path_input_folder, input_filename)
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

logging.info("Starting URL to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input file: {path_input_file}")
logging.info(f"Output folder: {path_output}")

# Check if URLs file exists
if not os.path.exists(path_input_file):
    logging.error(f"URL file not found in the input folder: {path_input_file}. Exiting.")
    sys.exit()

# Read URLs from the text file
try:
    with open(path_input_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
except Exception as e:
    logging.error(f"Failed to read URL file - {e}")
    sys.exit()

logging.info(f"Found {len(urls)} URL(s) to process.")

# Process each URL
for index, url in enumerate(urls, start=1):
    try:
        os.makedirs(path_output, exist_ok=True)
        output_filename = f"{timestamp}_url_{index}.pdf"
        output_path = os.path.join(path_output, output_filename)

        # Convert the URL to PDF
        logging.info(f"Converting URL to PDF: {url}")
        pdfkit.from_url(url, output_path)
        logging.info(f"PDF saved: {output_path}")

    except Exception as e:
        logging.error(f"Failed to convert {url} - {e}")

logging.info("URL to PDF Conversion Process Completed Successfully")
logging.info(f"Total URLs processed: {len(urls)}")
