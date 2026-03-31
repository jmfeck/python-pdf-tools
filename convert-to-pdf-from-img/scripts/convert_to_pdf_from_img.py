# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
import lazypdf as lz
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "Image to PDF Converter"

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

logging.info("Starting Image to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for image files in the input folder...")

# List of accepted image formats
accepted_formats = (".jpg", ".jpeg", ".png", ".tiff", ".bmp")
input_image_files = [f for f in os.listdir(path_input) if f.lower().endswith(accepted_formats)]
input_num_images = len(input_image_files)
logging.info(f"Found {input_num_images} image file(s) to process.")

# Check if there are any image files to process
if not input_image_files:
    logging.warning("No image files found in the input folder. Exiting the program.")
    sys.exit()

# Process each image file
for image_file in input_image_files:
    image_path = os.path.join(path_input, image_file)
    logging.info(f"Processing file: {image_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        output_filename = f"{timestamp}_{image_file.split('.')[0]}.pdf"
        output_path = os.path.join(path_output, output_filename)

        lz.read_images(image_path, page_size="fit").to_pdf(output_path)
        logging.info(f"Converted {image_file} to PDF at {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {image_file} - {e}")

logging.info("Image to PDF Conversion Process Completed Successfully")
logging.info(f"Total image files processed: {input_num_images}")
