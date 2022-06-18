from functools import wraps

from flask import jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.ApiKey import ApiKey
from Constant.Status import *

'''
Python Flask  API
Developed By : Mandeep Singh
'''

def isKeyAddedInRequest(key):
    def isKeyAdded(f):
        @wraps(f)
        def wrapper():
            print(f'key check: {key}')
            current_app.logger.info(f'key check: {key} on Request\n Url: {request.url}')
            if request.method == 'POST':
                requestPayloads = request.json
                if key not in requestPayloads:
                    return jsonify(
                        ApiResponse(Status.ABORT.value, "{} is required".format(key),
                                    dict()).__dict__), Status.ABORT.value
                else:
                    return f()
            elif request.method == 'GET':
                requestPayloads = request.args.get(key)
                print(f"request: {requestPayloads}")
                if key not in requestPayloads:
                    return jsonify(
                        ApiResponse(Status.ABORT.value, "{} is required".format(key),
                                    dict()).__dict__), Status.ABORT.value
                else:
                    return f()

        return wrapper

    return isKeyAdded


def isKeysAddedInRequest(keyList):
    def isKeyAdded(f):
        @wraps(f)
        def wrapper():
            if request.method == 'POST':
                requestPayloads = request.json
                print(f'Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                current_app.logger.info(f'Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                for key in keyList:
                    if key not in requestPayloads:
                        return jsonify(
                            ApiResponse(Status.ABORT.value, "{} is required".format(key),
                                        dict()).__dict__), Status.ABORT.value

                return f()

            elif request.method == 'GET':
                requestPayloads = request.args.keys()
                print(f'Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                current_app.logger.debug(f'Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                for key in keyList:
                    if key not in requestPayloads:
                        return jsonify(
                            ApiResponse(Status.ABORT.value, "{} is required".format(key),
                                        dict()).__dict__), Status.ABORT.value

                return f()

        return wrapper

    return isKeyAdded


def isAddressAddedInRequest(key):
    def isKeyAdded(f):
        @wraps(f)
        def wrapper():
            print(f'key check: {key}')
            if request.method == 'POST':
                requestPayloads = request.json
                if key not in requestPayloads:
                    apiResponse = ApiResponse(Status.error, "{} is required".format(key), dict())
                    return jsonify(apiResponse.__dict__), Status.error.value
                else:
                    address = requestPayloads[key]
                    print(f"Address in req: {address}")
                    if ApiKey.LOCATION_LAT.value not in address:
                        apiResponse = ApiResponse(Status.error, "{} is required".format(ApiKey.LOCATION_LAT.value),
                                                  dict())
                        return jsonify(apiResponse.__dict__), Status.error.value
                    elif ApiKey.LOCATION_LONG.value not in address:
                        apiResponse = ApiResponse(Status.error, "{} is required".format(ApiKey.LOCATION_LONG.value),
                                                  dict())
                        return jsonify(apiResponse.__dict__), Status.error.value
                    else:
                        return f()
            elif request.method == 'GET':
                requestPayloads = request.args.get(key)
                if key not in requestPayloads:
                    apiResponse = ApiResponse(Status.error, "{} is required".format(key), dict())
                    return jsonify(apiResponse.__dict__), Status.error.value
                else:
                    return f()

        return wrapper

    return isKeyAdded
