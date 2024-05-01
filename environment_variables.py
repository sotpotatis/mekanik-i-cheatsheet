"""environment_variables.py
Defines environment variables used throughout the code."""
import os
CONTENT_DIRECTORY = os.environ.get("ANKITEX_CONTENT_DIRECTORY", os.getcwd())
DOCUMENT_ENCODING = os.environ.get("ANKITEX_DOCUMENT_ENCODING", "UTF-8")
DATA_FILE_NAME = os.environ.get("ANKITEX_DATA_FILE_NAME", os.path.join(CONTENT_DIRECTORY, "tex2ankidata.json"))
OUTPUT_DIRECTORY = os.environ.get("ANKITEX_CONTENT_DIRECTORY", os.path.join(CONTENT_DIRECTORY, "flashcard_output"))