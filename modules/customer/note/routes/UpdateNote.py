import jwt
from flask import Blueprint, jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from AuthToken.JWTToken import JWTToken
from Constant.ApiKey import ApiKey
from Constant.Messages import Messages
from Constant.SqlConstant import SqlConstant
from Constant.Status import Status
from Database.DbConection import mydb
from Utils.Wrappers import CheckHeadersWrapper, CheckApiKeysWraaper, CheckDatabaseOperation

'''
Python Flask  API
Developed By : Mandeep Singh
'''

updateNote = Blueprint("updateNote", __name__)


@updateNote.route('updateNote', methods=['POST'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isAccessTokenHeaderAdded
@CheckApiKeysWraaper.isKeysAddedInRequest(
    [ApiKey.TITTLE.value, ApiKey.NOTEBOOK_TEXT.value, ApiKey.IS_FAVOURITE.value, ApiKey.IS_SECURE.value,
     ApiKey.NOTE_ID.value])
def UpdateNote():
    requestPayloads = request.json
    requestheaders = request.headers
    try:
        decodeUserData = JWTToken.decodeToken(requestheaders[ApiKey.ACCESS_TOKEN.value])
        print(decodeUserData)
        with mydb.cursor() as myconn:
            query = f'update {SqlConstant.TB_NOTE.value} set {SqlConstant.TITTLE.value} = %s, {SqlConstant.NOTEBOOK_TEXT.value} = %s,' \
                    f' {SqlConstant.IS_FAVOURITE.value} = %s, {SqlConstant.IS_SECURE.value} = %s where {SqlConstant.NOTE_ID.value} = %s and {SqlConstant.USER_ID.value} = %s'

            result = myconn.execute(query,
                                    (requestPayloads[ApiKey.TITTLE.value], requestPayloads[ApiKey.NOTEBOOK_TEXT.value],
                                     requestPayloads[ApiKey.IS_FAVOURITE.value],
                                     requestPayloads[ApiKey.IS_SECURE.value],
                                     requestPayloads[ApiKey.NOTE_ID.value],
                                     decodeUserData[ApiKey.CUS_ID.value]))
            mydb.commit()
            if result == 1:
                return CheckDatabaseOperation.getNoteData(requestPayloads[ApiKey.TITTLE.value],
                                                          decodeUserData[ApiKey.CUS_ID.value])
            else:
                return jsonify(ApiResponse(Status.ABORT.value, Messages.NOTE_NOT_UPDATE.value,
                                           dict()).__dict__), Status.ABORT.value

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
