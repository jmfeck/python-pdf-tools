# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import logging
from datetime import datetime
import comtypes.client  # for Windows-based Word to PDF conversion

# Program name for log prefix
PROGRAM_NAME = "DOC to PDF Converter"

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
logging.basicConfig(level=logging.INFO, format=log_format)

# Configure file handler with the same format
file_handler = logging.FileHandler(path_log)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

logging.info("Starting DOC to PDF Conversion Process")
logging.info(f"Timestamp: {timestamp}")
logging.info(f"Input folder: {path_input}")
logging.info(f"Output folder: {path_output}")
logging.info("Searching for DOC/DOCX files in the input folder...")

# List and count DOC/DOCX files
input_doc_files = [f for f in os.listdir(path_input) if f.endswith(".doc") or f.endswith(".docx")]
input_num_docs = len(input_doc_files)
logging.info(f"Found {input_num_docs} DOC/DOCX file(s) to process.")

# Check if there are any DOC/DOCX files to process
if not input_doc_files:
    logging.warning("No DOC/DOCX files found in the input folder. Exiting the program.")
    sys.exit()

# Process each DOC/DOCX file
for doc_file in input_doc_files:
    doc_path = os.path.join(path_input, doc_file)
    logging.info(f"Processing file: {doc_file}")

    try:
        os.makedirs(path_output, exist_ok=True)
        
        # Define the output path
        output_filename = f"{timestamp}_{doc_file.split('.')[0]}.pdf"
        output_path = os.path.join(path_output, output_filename)
        
        # Convert DOC/DOCX to PDF using comtypes (for Windows)
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 is the format code for PDF
        doc.Close()
        word.Quit()

        logging.info(f"Converted {doc_file} to PDF at {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {doc_file} - {e}")

logging.info("DOC to PDF Conversion Process Completed Successfully")
logging.info(f"Total DOC/DOCX files processed: {input_num_docs}")
