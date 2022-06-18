from functools import wraps
from flask import jsonify, request
from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.Status import *
from Constant.Messages import *
from Constant.ApiKey import *

'''
Python Flask  API
Developed By : Mandeep Singh
'''

def checkPostRequestMethod(f):
    @wraps(f)
    def wrapper():
        if request.method == 'POST':
            return f()
        else:
            return jsonify(ApiResponse(Status.TYPE_NOT_ALLOWED.value, Messages.TYPE_NOT_ALLOWED.value,
                                       dict()).__dict__), Status.TYPE_NOT_ALLOWED.value
    return wrapper


def checkGetRequestMethod(f):
    @wraps(f)
    def wrapper():
        if request.method == 'GET':
            return f()
        else:
            return jsonify(ApiResponse(Status.TYPE_NOT_ALLOWED.value, Messages.TYPE_NOT_ALLOWED.value,
                                       dict()).__dict__), Status.TYPE_NOT_ALLOWED.value
    return wrapper
