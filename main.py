"""main.py
Main script to create flashcards.
"""
import os, logging, parse_document, json
from pathlib import Path
from environment_variables import *
from data_file_handler import load_data_file, write_data_file
from class_definitions import AnkiDeck
from typing import Dict
from genanki import Package
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
# Find documents
logger.info("Finding documents...")
found_documents = []
for path in os.listdir(CONTENT_DIRECTORY):
    if Path(path).suffix == ".tex":
        logging.info(f"Found document {path} to process.")
        found_documents.append(os.path.join(CONTENT_DIRECTORY, path))
# Ensure path exists
if not os.path.exists(OUTPUT_DIRECTORY):
    logger.info("Creating output directory...")
    os.mkdir(OUTPUT_DIRECTORY)
    logger.info("Output directory created.")
# Load data file
if not os.path.exists(DATA_FILE_NAME):
    logger.info("Creating data file for storing Deck data...")
    data = {
        "decks": []
    }
    write_data_file(data)
else:
    data = load_data_file()
# Load decks
filenames_to_decks : Dict[str, AnkiDeck] = {}
for deck_json in data["decks"]:
    loaded_deck = AnkiDeck().__from_json__(deck_json)
    filenames_to_decks[loaded_deck.filename] = loaded_deck
# Process them
for document in found_documents:
    logger.info(f"Processing {document}...")
    document_content = open(document, "r", encoding=DOCUMENT_ENCODING).read()
    # Find preamble
    preamble = parse_document.find_latex_preamble(document_content)
    assets = parse_document.find_latex_assets(document_content)
    logger.info(f"Found LaTeX assets: {assets} in document")
    # Find corresponding deck
    if document not in filenames_to_decks:
        logger.info(f"Creating new deck for {document}...")
        new_deck = AnkiDeck(name=f"Deck for filename {document}", filename=document, latex_preamble=preamble)
        filenames_to_decks[document] = new_deck
    else:
        logger.info(f"Found previous deck to use for {document}...")
    if filenames_to_decks[document].latex_preamble != preamble:
        logger.info(f"Found new LaTeX preamble for {document}, adding...")
        filenames_to_decks[document].latex_preamble = preamble
    found_flashcards = parse_document.find_all_flashcards_in_latex_code(
        document_content, parent_deck=filenames_to_decks[document]
    )
    logger.info(f"Found {len(found_flashcards)} flashcards in the document.")
    # For each flashcard, write back the GUID to the LaTeX file
    for found_flashcard in found_flashcards:
        flashcard_guid_string = f"{parse_document.FLASHCARD_GUID_COMMENT_PREFIX} {found_flashcard.guid}"
        if flashcard_guid_string not in document_content:
            document_content = document_content.replace(
                found_flashcard.full_match,
                f"\n{flashcard_guid_string}\n{found_flashcard.full_match}"
            )
    filenames_to_decks[document].flashcards = found_flashcards
        
    logger.info(f"Keeping LaTeX file in sync; writing new content...")
    open(document, "w", encoding=DOCUMENT_ENCODING).write(document_content)
    logger.info(f"LaTeX file {document} synced.")
    # Write deck to Anki file
    created_package = Package(filenames_to_decks[document].__to_anki__())
    created_package.media_files = assets
    logger.info("Writing package... if you get an error, ensure all your images are defined!")
    created_package.write_to_file(
        os.path.join(OUTPUT_DIRECTORY, f"{document.replace('.', '')}-deck.apkg")
    )
    logger.info(f"Done processing {document}!") 
data["decks"] = [
    deck.__to_json__() for deck in filenames_to_decks.values()
]

write_data_file(data)