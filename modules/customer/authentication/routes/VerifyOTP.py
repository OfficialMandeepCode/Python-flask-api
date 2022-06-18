from flask import Blueprint, jsonify, request, current_app
from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.ApiKey import ApiKey
from Constant.Messages import Messages
from Constant.SqlConstant import SqlConstant
from Constant.Status import Status
from DataModels.Customer.Users.UserDataClass import User
from Database.DbConection import mydb
from Utils.Wrappers import CheckHeadersWrapper, CheckApiKeysWraaper
from AuthToken.JWTToken import JWTToken

'''
Python Flask  API
Developed By : Mandeep Singh
'''

# /api/customer/authinfo/auth/verifyOtp
verifyOtp = Blueprint("verifyOtp", __name__)

@verifyOtp.route('verifyOtp', methods=['POST'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isContentTypeHeaderAdded
@CheckApiKeysWraaper.isKeysAddedInRequest([ApiKey.OTP_CODE.value, ApiKey.CUS_ID.value])
def VerifyOtp():
    requestPayloads = request.json
    try:
        with mydb.cursor() as myconn:
            query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.USER_ID.value} = %s'
            # and {SqlConstant.OTP_CODE.value} = %s
            myconn.execute(query, (requestPayloads[ApiKey.CUS_ID.value]))
            result = myconn.fetchone()

    except Exception as e:
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
    print(result)
    if result is not None:
        if result[8] != requestPayloads[ApiKey.OTP_CODE.value]:
            return jsonify(ApiResponse(Status.ABORT.value, Messages.INVALID_OTP.value,
                                       dict()).__dict__), Status.ABORT.value

        elif result[8] == requestPayloads[ApiKey.OTP_CODE.value]:
            try:
                with mydb.cursor() as myconn:
                    query = f'update {SqlConstant.TB_USER.value} set {SqlConstant.IS_PHONE_VERIFIED.value} = %s where {SqlConstant.USER_ID.value} = %s'
                    myconn.execute(query, (1, requestPayloads[ApiKey.CUS_ID.value]))
                    mydb.commit()

                    query = f'select * from {SqlConstant.TB_USER.value} where {SqlConstant.USER_ID.value} = %s'
                    myconn.execute(query, (requestPayloads[ApiKey.CUS_ID.value]))
                    result = myconn.fetchone()
                    if result is not None:
                        # (1, None, 'api@yopmail.com', '62392874119', 'abcdefghijlmnpqrstuvwxyz', None, datetime.datetime(2022, 4, 4, 0, 0), 91, 1111)
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

                        return jsonify(ApiResponse(Status.SUCCESS.value, Messages.EXECUTION_SUCCESSFULLY.value,
                                                   userModel.__dict__).__dict__), Status.SUCCESS.value
                    else:
                        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                                   dict()).__dict__), Status.ABORT.value

            except Exception as e:
                return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                           dict()).__dict__), Status.ABORT.value

        else:
            print("error")
            return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                       dict()).__dict__), Status.ABORT.value
    else:
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
