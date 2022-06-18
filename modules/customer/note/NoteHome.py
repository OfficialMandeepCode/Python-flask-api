from flask import Blueprint, jsonify, request,current_app
from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.Messages import Messages
from Constant.Status import Status
from .routes.AddNotes import addNote
from .routes.UpdateNote import updateNote
from .routes.DeleteNote import deleteNote
from .routes.GetAllNote import allNote
'''
Python Flask  API
Developed By : Mandeep Singh
'''

#/api/customer/note
noteHome = Blueprint("noteHome", __name__)

noteHome.register_blueprint(addNote, url_prefix='note/')
noteHome.register_blueprint(updateNote, url_prefix='note/')
noteHome.register_blueprint(deleteNote, url_prefix='note/')
noteHome.register_blueprint(allNote, url_prefix='note/')


@noteHome.route('note')
def note_Home():
    current_app.logger.info(f'{Messages.WELCOME_AUTH_HOME.value}\n Url: %s', request.url)
    return jsonify(ApiResponse(Status.SUCCESS.value, Messages.WELCOME_AUTH_HOME.value,
                               dict()).__dict__), Status.SUCCESS.value
