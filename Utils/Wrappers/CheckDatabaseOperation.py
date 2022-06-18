from functools import wraps

import jwt
from flask import jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from AuthToken.JWTToken import JWTToken
from Constant.ApiKey import *
from Constant.Messages import *
from Constant.SqlConstant import SqlConstant
from Constant.Status import *
from DataModels.Customer.Notes.NoteDataClass import Note
from DataModels.Customer.Users.UserDataClass import User
from Database.DbConection import mydb
'''
Python Flask  API
Developed By : Mandeep Singh
'''
def isUserExistInRecords():
    def userExist(f):
        @wraps(f)
        def wrapper():
            if request.method == 'POST':
                requestPayloads = request.json
                current_app.logger.info(
                    f'isUserExistInRecords Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                with mydb.cursor() as myconn:
                    query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.EMAIL_ID.value} = %s and {SqlConstant.PHONE_NUMBER.value} = %s'
                    myconn.execute(query,
                                   (requestPayloads[ApiKey.EMAIL_ID.value], requestPayloads[ApiKey.PHONE_NUMBER.value]))
                    result = myconn.fetchone()
                    mydb.commit()
                print(result)
                if result is not None:
                    if (len(result) >= 1):
                        jwtPayload = {
                            f'{ApiKey.CUS_ID.value}': result[0],
                            f'{ApiKey.CUS_NAME.value}': result[1],
                            f'{ApiKey.EMAIL_ID.value}': result[2],
                            f'{ApiKey.PHONE_NUMBER.value}': result[3],
                            f'{ApiKey.DEVICE_TOKEN.value}': result[4]
                        }
                        userModel = User(cusId=result[0], name=result[1], emailId=result[2], phoneNumber=result[3],
                                         deviceToken=result[4],
                                         authToken=JWTToken.generateToken(jwtPayload) if result[9] == 1 else "",
                                         countryCode=result[7], otpCode=result[8], isPhoneVerified=result[9])

                        return jsonify(ApiResponse(Status.SUCCESS.value, Messages.EXECUTION_SUCCESSFULLY.value,
                                                   userModel.__dict__).__dict__), Status.SUCCESS.value
                    else:
                        return f()
                else:
                    return f()

        return wrapper

    return userExist


def isEmailIdExistInRecords():
    def emailExist(f):
        @wraps(f)
        def wrapper():
            if request.method == 'POST':
                requestPayloads = request.json
                current_app.logger.info(
                    f'isUserExistInRecords Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                with mydb.cursor() as myconn:
                    query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.EMAIL_ID.value} = %s'
                    myconn.execute(query,
                                   (requestPayloads[ApiKey.EMAIL_ID.value]))
                    result = myconn.fetchone()
                    mydb.commit()
                print(result)
                if result is not None:
                    return jsonify(ApiResponse(Status.ABORT.value, Messages.ALREADY_EMAIL_ID_EXIST.value,
                                               dict()).__dict__), Status.ABORT.value
                else:
                    return f()

        return wrapper

    return emailExist


def isPhoneNumExistInRecords():
    def phoneNumExist(f):
        @wraps(f)
        def wrapper():
            if request.method == 'POST':
                requestPayloads = request.json
                current_app.logger.info(
                    f'isUserExistInRecords Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')
                with mydb.cursor() as myconn:
                    query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.PHONE_NUMBER.value} = %s'
                    myconn.execute(query,
                                   (requestPayloads[ApiKey.PHONE_NUMBER.value]))
                    result = myconn.fetchone()
                    mydb.commit()
                print(result)
                if result is not None:
                    return jsonify(ApiResponse(Status.ABORT.value, Messages.ALREADY_PHONE_NUM_EXIST.value,
                                               dict()).__dict__), Status.ABORT.value
                else:
                    return f()

        return wrapper

    return phoneNumExist


def isNoteExistInRecords():
    def noteExist(f):
        @wraps(f)
        def wrapper():
            if request.method == 'POST':
                try:
                    requestPayloads = request.json
                    requestheaders = request.headers
                    decodeUserData = JWTToken.decodeToken(requestheaders[ApiKey.ACCESS_TOKEN.value])
                    # current_app.logger.info(
                    #     f'isUserExistInRecords Payloads In Request: {requestPayloads} On Request\n Url: {request.url}')

                    with mydb.cursor() as myconn:
                        query = f'select * from {SqlConstant.TB_NOTE.value} where {SqlConstant.TITTLE.value} = %s AND {SqlConstant.USER_ID.value} = %s'
                        myconn.execute(query,
                                       (requestPayloads[ApiKey.TITTLE.value], decodeUserData[ApiKey.CUS_ID.value]))
                        result = myconn.fetchone()
                        mydb.commit()
                    print(result)
                    if result is not None:
                        if (len(result) >= 1):

                            noteModel = Note(noteId=result[0], title=result[1], notebookText=result[2],
                                             isFavourite=result[3], isSecure=result[4], createdAt=result[5],
                                             lastUpdateAt=result[6])

                            return jsonify(ApiResponse(Status.ABORT.value, Messages.NOTE_ALREADY_EXISTING.value,
                                                       dict()).__dict__), Status.ABORT.value
                        else:
                            return f()
                    else:
                        return f()

                except jwt.ExpiredSignatureError as err:
                    print(f'Exception: {err}')
                    current_app.logger.error(f'Errror: {err} on Request\n Url: {request.url}')
                    return jsonify(ApiResponse(Status.UN_AUTHORISED.value, Messages.TOKEN_EXPIRED.value,
                                               dict()).__dict__), Status.UN_AUTHORISED.value

                except Exception as e:
                    print(f'Exception: {e}')
                    current_app.logger.error(f'Errror: {e} on Request\n Url: {request.url}')
                    return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                               dict()).__dict__), Status.ABORT.value

        return wrapper

    return noteExist


def getNoteData(title, cusId):
    # print(f"Noteid: {noteId}")
    with mydb.cursor() as myconn:
        # if not noteId:
        query = f'select * from {SqlConstant.TB_NOTE.value} where {SqlConstant.TITTLE.value} = %s AND {SqlConstant.USER_ID.value} = %s'
        myconn.execute(query, (title, cusId))
    result = myconn.fetchone()
    print(result)
    if result is not None:
        noteModel = Note(noteId=result[0], title=result[1], notebookText=result[2], isFavourite=result[3],
                         isSecure=result[4], createdAt=result[5], lastUpdateAt=result[6])
        return jsonify(ApiResponse(Status.SUCCESS.value, Messages.EXECUTION_SUCCESSFULLY.value,
                                   noteModel.__dict__).__dict__), Status.SUCCESS.value
    else:
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
