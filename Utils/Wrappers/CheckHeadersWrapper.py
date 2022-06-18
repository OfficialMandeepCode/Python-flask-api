from functools import wraps
from flask import jsonify, request
from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.Status import *
from Constant.Messages import *
from Constant.ApiKey import *

''' Wrapper Method to check is Content Language Header added in request or not'''

'''
Python Flask  API
Developed By : Mandeep Singh
'''

def isContentLanguageHeaderAdded(f):
    @wraps(f)
    def wrapper():
        requestheaders = request.headers
        if ApiKey.CONTENT_LANGUAGE.value not in requestheaders:
            return jsonify(ApiResponse(Status.ABORT, "{} header is required".format(ApiKey.CONTENT_LANGUAGE.value),
                                       dict()).__dict__), Status.ABORT.value
        else:
            return f()

    return wrapper


''' Wrapper Method to check is Content Type Header added in request or not'''


def isContentTypeHeaderAdded(f):
    @wraps(f)
    def wrapper():
        requestheaders = request.headers
        if ApiKey.CONTENT_TYPE.value not in requestheaders:
            return jsonify(ApiResponse(Status.ABORT, "{} header is required".format(ApiKey.CONTENT_TYPE.value),
                                       dict()).__dict__), Status.ABORT.value
        else:
            return f()

    return wrapper


''' Wrapper Method to check is Access Token Header added in request or not'''


def isAccessTokenHeaderAdded(f):
    @wraps(f)
    def wrapper():
        requestheaders = request.headers
        if ApiKey.ACCESS_TOKEN.value not in requestheaders:
            return jsonify(ApiResponse(Status.ABORT, "{} header is required".format(ApiKey.ACCESS_TOKEN.value),
                                       dict()).__dict__), Status.ABORT.value
        else:
            return f()

    return wrapper
