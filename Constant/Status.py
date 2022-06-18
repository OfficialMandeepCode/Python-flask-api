import enum
'''
Python Flask  API
Developed By : Mandeep Singh
'''

class Status(enum.IntEnum):
    SUCCESS = 200
    ABORT = 400
    UN_AUTHORISED = 401
    TYPE_NOT_ALLOWED = 405
    NOT_FOUND = 404
