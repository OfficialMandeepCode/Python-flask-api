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
# /api/customer/authinfo/auth/resendOtp
updateProfile = Blueprint("updateProfile", __name__)


@updateProfile.route('updateProfile', methods=['POST'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isContentTypeHeaderAdded
@CheckHeadersWrapper.isAccessTokenHeaderAdded
@CheckApiKeysWraaper.isKeysAddedInRequest(
    [ApiKey.CUS_NAME.value, ApiKey.EMAIL_ID.value, ApiKey.COUNTRY_CODE.value, ApiKey.PHONE_NUMBER.value])
def UpdateProfile():
    requestPayloads = request.json
    requestheaders = request.headers
    try:
        decodeUserData = JWTToken.decodeToken(requestheaders[ApiKey.ACCESS_TOKEN.value])
        print(decodeUserData)
        with mydb.cursor() as myconn:
            query = f'update {SqlConstant.TB_USER.value} set {SqlConstant.EMAIL_ID.value} = %s, {SqlConstant.NAME.value} = %s, {SqlConstant.COUNTRY_CODE.value} = %s,{SqlConstant.PHONE_NUMBER.value} = %s where {SqlConstant.USER_ID.value} = %s'
            myconn.execute(query, (requestPayloads[ApiKey.EMAIL_ID.value], requestPayloads[ApiKey.CUS_NAME.value],
                                   requestPayloads[ApiKey.COUNTRY_CODE.value],
                                   requestPayloads[ApiKey.PHONE_NUMBER.value], decodeUserData[ApiKey.CUS_ID.value]))
            mydb.commit()

            return jsonify(ApiResponse(Status.SUCCESS.value, Messages.PROFILE_UPDATE.value,
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
