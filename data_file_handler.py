"""data_file_handler.py
Handles reading data from the data file"""
from environment_variables import DATA_FILE_NAME, DOCUMENT_ENCODING
import json
def load_data_file()->dict:
    """Load contents from the data file into memory."""
    return json.loads(open(DATA_FILE_NAME, "r", encoding=DOCUMENT_ENCODING).read())

def write_data_file(input_data:dict)->None:
    """Write contents to the data file."""
    with open(DATA_FILE_NAME, "w", encoding=DOCUMENT_ENCODING) as data_file:
        data_file.write(json.dumps(input_data))