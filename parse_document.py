"""parse_document.py
Contains helper code to parse a document.
This is where the main magic happens."""
import os, re, logging
from class_definitions import Flashcard, AnkiDeck
from typing import List, Optional
MAGIC_REGEX = r"\\begin{ankiflashcard}({[\S ]*})*([\S\s]+?(?=\\end{ankiflashcard}))"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
FLASHCARD_GUID_COMMENT_PREFIX = "% DONOTREMOVE ANKI-FLASHCARD GUID" # See below
def find_all_flashcards_in_latex_code(input_code:str, parent_deck:Optional[AnkiDeck]=None)->List[Flashcard]:
    """Finds all the Flashcards referenced in a piece of LaTeX code.
    
    :param input_code A raw LaTeX document as input.

    :param parent_deck: The parent deck. If not sent, the parent deck may be loaded if the deck is loaded from a JSON
    file.
    
    :returns A list of flashcards that are referenced in the code."""
    lines = [] # List of lines in format (line_end (character), line_content)
    i = 0
    line = ""
    for character in input_code:
        if character == "\n":
            lines.append((i, line))
            line = ""
        else:
            line += character
        i += 1
    matches = re.finditer(MAGIC_REGEX, input_code)
    found_flashcards = []
    for regex_match in iter(matches):
        question, latex_code = regex_match.groups()
        #Check if the above line is a GUID
        #We set GUIDs with a comment: % ANKI-FLASHCARD GUID
        close_line = ""
        for line_index, line_content in lines:
            if line_index < regex_match.start():
                close_line = line_content
        if close_line.startswith(FLASHCARD_GUID_COMMENT_PREFIX):
            logger.debug(f"Loading flashcard GUID from line {close_line}...")
            guid = int(close_line.strip().replace(FLASHCARD_GUID_COMMENT_PREFIX, "")[1:]) # There will be a trailing whitespace to handle, hence [1:]
        else:
            logger.debug(f"Flashcard with question {question} and above line {close_line} missing GUID.")
            guid = None
        if question is not None:
            # Replace LaTeX comments
            question = question.replace("{", "").replace("}", "")
        logger.info(f"Found flashcard with question {question} and GUID {guid}.")
        found_flashcard = Flashcard(
            guid=guid,
            question=question,
            full_match=regex_match.group(),
            parent=parent_deck,
            latex_code=latex_code
        )
        found_flashcards.append(found_flashcard)
    return found_flashcards


def find_latex_preamble(input_code:str)->str:
    """Finds the relevant code in a LaTeX document that is related to the preamble."""
    preamble_content = input_code.split("\\begin{document}")[0]
    return preamble_content

def find_latex_assets(input_code:str)->List[str]:
    """Finds all the LaTeX assets referenced in a file."""
    LATEX_ASSET_REGEX = r"\\includegraphics(\[\S+\]*){([A-Za-z.åäöÅÄÖ\-_ ]+)}*"
    matches = re.finditer(LATEX_ASSET_REGEX, input_code)
    return [
        matched_asset_reference.groups()[1] for matched_asset_reference in matches
        #Group 1 contains the filename
    ]