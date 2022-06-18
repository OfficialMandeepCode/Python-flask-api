"""
Python Flask  API
Developed By : Mandeep Singh
"""

class NoteAll():
    notesCount = 0
    note = []

    def __init__(self, noteCount = 0, noteList = []):
        self.notesCount = noteCount
        self.note = noteList

