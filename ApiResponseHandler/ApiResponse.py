
"""
Python Flask  API
Developed By : Mandeep Singh
"""

class ApiResponse:
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

