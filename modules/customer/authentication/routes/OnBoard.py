from flask import Blueprint, jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from AuthToken.JWTToken import JWTToken
from Constant.ApiKey import ApiKey
from Constant.Messages import Messages
from Constant.SqlConstant import SqlConstant
from Constant.Status import Status
from DataModels.Customer.Users.UserDataClass import User
from Database.DbConection import mydb
from Utils.Wrappers import CheckHeadersWrapper, CheckApiKeysWraaper, CheckDatabaseOperation

# /api/customer/authinfo/auth/onBoard
onBoard = Blueprint("onBoard", __name__)
'''
Python Flask  API
Developed By : Mandeep Singh
'''

@onBoard.route('onBoard', methods=['POST'])
@CheckHeadersWrapper.isContentTypeHeaderAdded
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckApiKeysWraaper.isKeysAddedInRequest(
    [ApiKey.COUNTRY_CODE.value, ApiKey.PHONE_NUMBER.value, ApiKey.DEVICE_TOKEN.value, ApiKey.EMAIL_ID.value,
     ApiKey.CUS_NAME.value])
@CheckDatabaseOperation.isUserExistInRecords()
@CheckDatabaseOperation.isEmailIdExistInRecords()
@CheckDatabaseOperation.isPhoneNumExistInRecords()
def authOnBoard():
    requestPayloads = request.json
    current_app.logger.info(f'Payload -> {requestPayloads} on Request\n URL: {request.url}')
    try:
        with mydb.cursor() as myconn:
            query = f"insert into {SqlConstant.TB_USER.value} ({SqlConstant.EMAIL_ID.value}, {SqlConstant.PHONE_NUMBER.value}," \
                    f" {SqlConstant.DEVICE_TOKEN.value}, {SqlConstant.COUNTRY_CODE.value}, {SqlConstant.OTP_CODE.value}, {SqlConstant.NAME.value}) values(%s,%s,%s,%s,%s,%s)"
            myconn.execute(query,
                           (requestPayloads[ApiKey.EMAIL_ID.value], requestPayloads[ApiKey.PHONE_NUMBER.value],
                            requestPayloads[ApiKey.DEVICE_TOKEN.value], requestPayloads[ApiKey.COUNTRY_CODE.value],
                            "1111", requestPayloads[ApiKey.CUS_NAME.value]))
            mydb.commit()
            current_app.logger.info(
                f'User Created {requestPayloads[ApiKey.EMAIL_ID.value]} on request\n URL: {request.url}')

            query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.EMAIL_ID.value} = %s AND {SqlConstant.PHONE_NUMBER.value} = %s'
            myconn.execute(query, (requestPayloads[ApiKey.EMAIL_ID.value], requestPayloads[ApiKey.PHONE_NUMBER.value]))
            result = myconn.fetchone()
            if result is not None:
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
                                 countryCode=result[7],
                                 otpCode=result[8], isPhoneVerified=result[9])

                return jsonify(ApiResponse(Status.SUCCESS.value, Messages.SEND_OTP.value,
                                           userModel.__dict__).__dict__), Status.SUCCESS.value
            else:
                return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                           dict()).__dict__), Status.ABORT.value


    except Exception as e:
        print(f'MySQl Errror: {e}')
        current_app.logger.error(f'MySQl Errror: {e} on Request\n Url: {request.url}')
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
