"""guid_handler.py
Each Anki flashcard has a unique GUID.
To allow the application to easily update GUIDs, it needs to (at the first time)
add the GUID of each question in the LaTeX file. It also subsequently
needs to keep track of them."""
import os, regex
