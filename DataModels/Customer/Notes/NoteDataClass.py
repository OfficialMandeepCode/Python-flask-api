"""
Python Flask  API
Developed By : Mandeep Singh
"""
class Note():
    noteId = ""
    title = ""
    notebookText = ""
    isFavourite = ""
    isSecure = ""
    lastUpdateAt = ""
    createdAt = ""



    def __init__(self, noteId, title, notebookText, isFavourite, isSecure, lastUpdateAt, createdAt):
        self.noteId = noteId
        self.title = title
        self.notebookText = notebookText
        self.isFavourite = isFavourite
        self.isSecure = isSecure
        self.createdAt = createdAt
        self.lastUpdateAt = lastUpdateAt

