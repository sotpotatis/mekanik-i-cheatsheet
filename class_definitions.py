"""class_definitions.py
Defines the classes used in the code."""
import random, logging, html
from genanki import BASIC_MODEL, Note, Deck, Model
from typing import Optional, List


logging.basicConfig(level=logging.DEBUG)

class AnkiDeck:
    """Defines an Anki deck."""
    def __init__(self, id:Optional[int]=None, filename:Optional[str]=None, name:Optional[str]=None, flashcards:Optional[List["Flashcard"]]=None, latex_preamble:Optional[str]=None) -> None:
        if id is None:
            id = self.generate_anki_id()
        self.id = id
        self.name = name
        self.filename = filename # File that the deck belongs to
        self.latex_preamble = None # Preamble of LaTeX document
        self.logger = logging.getLogger(f"{__name__}.ankiDeck.{id}")
        if flashcards is not None:
            for flashcard in flashcards:
                flashcard.parent = self
        else:
            flashcards = []
        self.flashcards = flashcards

    def generate_anki_id(self)->int:
        """Generates an Anki ID according to the genanki docs."""
        return random.randrange(1 << 30, 1 << 31)
    
    def generate_anki_note_guid(self):
        """Generates a unique note GUID."""
        taken_note_guids = [flashcard.guid for flashcard in self.flashcards]
        note_id = self.generate_anki_id()
        while note_id in taken_note_guids:
            self.logger.warning(f"Regerating note {note_id}, already in taken note IDs")
            note_id = self.generate_anki_id()
        return note_id

    def __to_anki__(self)->Deck:
        """Returns an Anki deck from the current state of the AnkiDeck class."""
        deck_output = Deck(self.id, self.name)
        self.logger.info(f"Assembling deck \"{self.name}\" (with ID {self.id})...")
        for flashcard in self.flashcards:
            self.logger.info(f"Adding card {flashcard} to Anki deck...")
            deck_output.add_note(flashcard.__to_anki__())
        self.logger.info("Deck assembled.")
        return deck_output

    def __to_json__(self)->dict:
        """Returns JSON-serializable data for writing the AnkiDeck to a JSON file for later saving."""
        return {
            "deck_name": self.name,
            "filename": self.filename,
            "id": self.id,
            "flashcards": [flashcard.__to_json__() for flashcard in self.flashcards],
            "preamble": self.latex_preamble
        }
    
    def __from_json__(self, input_json:dict)->None:
        """Loads an AnkiDeck from JSON data into self."""
        self.id = input_json["id"]
        self.name = input_json["deck_name"]
        self.filename = input_json["filename"]
        self.latex_preamble = input_json["preamble"]
        self.flashcards = [
        ]
        for flashcard_json in input_json["flashcards"]:
            loaded_flashcard = Flashcard().__from_json__(flashcard_json)
            loaded_flashcard.parent = self
            self.flashcards.append(
                loaded_flashcard
            )
        
        self.logger.info(f"Loaded {len(self.flashcards)} flashcards from JSON.")
        return self

class Flashcard:
    """Defines a flashcard as defined in the code."""
    def __init__(self, latex_code:Optional[str]=None, full_match:Optional[None]=None, question:Optional[None]=None, guid:Optional[None]=None, parent:Optional[None]=None) -> None:
        self.latex_code = latex_code
        self.full_match = full_match
        if self.latex_code is not None:
            # Use common replacements in LaTeX code
            self.ensure_latex_code_is_anki_compatible(self.latex_code)
            self.html_escaped_latex_code = html.escape(self.latex_code)
        else:
            self.html_escaped_latex_code = None
        self.question = question
        self.parent = parent
        if guid is None and self.parent is not None:
            guid = self.parent.generate_anki_note_guid()
        self.guid = guid
        if question is None:
            self.question = f"Question {self.guid}"
        self.logger = logging.getLogger(f"{__name__}.Flashcard.{guid}")

    def __to_anki__(self)->Note:
        """Converts a Flashcard to an Anki-compatible one."""
        # Include a custom LaTeX preamble with the dependent packages
        note_model = BASIC_MODEL
        if self.parent is not None and self.parent.latex_preamble is not None:
            # A little hacky, but add the Anki default preamble below so that any relevant
            # overrides come through
            note_model.latex_pre = "\\documentclass[12pt]{article}" + self.parent.latex_preamble + r"""
            \special{papersize=3in,5in}
            \usepackage[utf8]{inputenc}
            \usepackage{amssymb,amsmath}
            \pagestyle{empty}
            \setlength{\parindent}{0in}""" # This is basically the default LaTeX that genanki uses
        return Note(
            guid=self.guid,
            model=BASIC_MODEL,
            fields=[self.question, f"[latex]{self.html_escaped_latex_code}[/latex]"]
        )
    def ensure_latex_code_is_anki_compatible(self, input_code:str)->str:
        """Ensures that the LaTeX code input is compatible with the LaTeX intepreter Anki
        uses. TODO implement!"""
        return input_code
    
    def __to_json__(self)->dict:
        """Returns JSON-serializable data for writing the Flashcard to a JSON file for later saving."""
        return {
            "guid": self.guid,
            "latex": self.html_escaped_latex_code,
            "question": self.question
        }
    
    def __from_json__(self, input_json:dict)->None:
        """Loads a Flashcard from JSON data into self."""
        self.guid = input_json["guid"]
        self.question = input_json["question"]
        # LaTeX code is stored in JSON like it is in Anki,
        # aka. as escaped HTML code (so we need to decrypt it)
        self.html_escaped_latex_code = input_json["latex"]
        self.latex = html.unescape(self.html_escaped_latex_code)
        self.logger.info(f"Loaded new flashcard {self.guid} from JSON.")
        return self

    def __str__(self)->str:
        return f"Card GUID {self.guid}, question {self.question}"