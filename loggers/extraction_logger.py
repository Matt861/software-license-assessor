import logging
import os
from pathlib import Path

p = Path(__file__).resolve()

# Create a custom logger
extraction_logger = logging.getLogger(__name__)
extraction_logger.setLevel(logging.DEBUG)  # Set the minimum logging level

# Create handlers for file and console
file_hander_path = os.path.join(p.parent.parent, "logs/file_extraction.log")
file_handler = logging.FileHandler(file_hander_path, mode='w')
console_handler = logging.StreamHandler()

# Set the logging level for each handler
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.DEBUG)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
extraction_logger.addHandler(file_handler)
extraction_logger.addHandler(console_handler)