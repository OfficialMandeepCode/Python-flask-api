import jwt
from flask import Blueprint, jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from AuthToken.JWTToken import JWTToken
from Constant.ApiKey import ApiKey
from Constant.Messages import Messages
from Constant.SqlConstant import SqlConstant
from Constant.Status import Status
from Database.DbConection import mydb
from Utils.Wrappers import CheckHeadersWrapper, CheckApiKeysWraaper

'''
Python Flask  API
Developed By : Mandeep Singh
'''

deleteNote = Blueprint("deleteNote", __name__)


@deleteNote.route('deleteNote', methods=['POST'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isAccessTokenHeaderAdded
@CheckApiKeysWraaper.isKeysAddedInRequest([ApiKey.NOTE_ID.value])
def DeleteNote():
    requestPayloads = request.json
    requestheaders = request.headers
    try:
        decodeUserData = JWTToken.decodeToken(requestheaders[ApiKey.ACCESS_TOKEN.value])
        print(decodeUserData)
        with mydb.cursor() as myconn:
            query = f'delete from {SqlConstant.TB_NOTE.value} where {SqlConstant.NOTE_ID.value} = %s and {SqlConstant.USER_ID.value} = %s'

            myconn.execute(query, (requestPayloads[ApiKey.NOTE_ID.value], decodeUserData[ApiKey.CUS_ID.value]))
            mydb.commit()
            return jsonify(ApiResponse(Status.SUCCESS.value, Messages.NOTE_DELETE.value,
                                       dict()).__dict__), Status.SUCCESS.value

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
