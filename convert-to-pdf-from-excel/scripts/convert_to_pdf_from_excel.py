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
import win32com.client as win32
from datetime import datetime

# Program name for log prefix
PROGRAM_NAME = "Excel to PDF Converter"

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

logging.info("Starting Excel to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for Excel files in the input folder...")

# List and count Excel files
input_excel_files = [f for f in os.listdir(path_input) if f.endswith((".xlsx", ".xls"))]
input_num_excels = len(input_excel_files)
logging.info(f"Found {input_num_excels} Excel file(s) to process.")

# Check if there are any Excel files to process
if not input_excel_files:
    logging.warning("No Excel files found in the input folder. Exiting the program.")
    sys.exit()

# Process each Excel file
excel_app = win32.gencache.EnsureDispatch("Excel.Application")
excel_app.Visible = False

for excel_file in input_excel_files:
    excel_path = os.path.join(path_input, excel_file)
    logging.info(f"Processing file: {excel_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        workbook = excel_app.Workbooks.Open(excel_path)
        
        # Define the output PDF file path
        output_filename = f"{timestamp}_{excel_file.split('.')[0]}.pdf"
        output_path = os.path.join(path_output, output_filename)

        # Save workbook as PDF
        workbook.ExportAsFixedFormat(0, output_path)
        logging.info(f"Converted {excel_file} to PDF at {output_path}")

        # Close the workbook without saving changes
        workbook.Close(False)

    except Exception as e:
        logging.error(f"Failed to process {excel_file} - {e}")

# Quit the Excel application
excel_app.Quit()

logging.info("Excel to PDF Conversion Process Completed Successfully")
logging.info(f"Total Excel files processed: {input_num_excels}")
