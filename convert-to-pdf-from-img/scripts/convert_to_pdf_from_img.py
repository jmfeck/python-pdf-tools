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
from PIL import Image
import fitz  # PyMuPDF

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
        
        # Open the image using Pillow
        with Image.open(image_path) as img:
            # Convert image to RGB (strip transparency if necessary) for PDF compatibility
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                logging.info(f"Converting image {image_file} from {img.mode} to RGB")
                img_rgb = Image.new("RGB", img.size, (255, 255, 255))  # White background
                img_rgb.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
            else:
                img_rgb = img.convert("RGB")

            width, height = img_rgb.size
            
            # Create a new PDF document and add a page with the image dimensions
            output_filename = f"{timestamp}_{image_file.split('.')[0]}.pdf"
            output_path = os.path.join(path_output, output_filename)
            
            doc = fitz.open()  # Create a new PDF
            page = doc.new_page(width=width, height=height)

            # Save image as a temporary JPEG file to insert into PDF
            temp_image_path = "temp_image.jpg"
            img_rgb.save(temp_image_path, "JPEG")
            img_pixmap = fitz.Pixmap(temp_image_path)
            
            # Insert the image as a full-page in the PDF
            page.insert_image(fitz.Rect(0, 0, width, height), pixmap=img_pixmap)
            
            # Save and clean up
            doc.save(output_path)
            doc.close()
            os.remove(temp_image_path)  # Remove temporary image file
            
            logging.info(f"Converted {image_file} to PDF at {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {image_file} - {e}")

logging.info("Image to PDF Conversion Process Completed Successfully")
logging.info(f"Total image files processed: {input_num_images}")
