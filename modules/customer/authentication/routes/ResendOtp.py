from flask import Blueprint, jsonify, request

from ApiResponseHandler.ApiResponse import ApiResponse
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
resendOtp = Blueprint("resendOtp", __name__)


@resendOtp.route('resendOtp', methods=['POST'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isContentTypeHeaderAdded
@CheckApiKeysWraaper.isKeyAddedInRequest(ApiKey.CUS_ID.value)
def ResendOtp():
    requestPayloads = request.json
    try:
        with mydb.cursor() as myconn:
            query = f'update {SqlConstant.TB_USER.value} set {SqlConstant.OTP_CODE.value} = %s where {SqlConstant.USER_ID.value} = %s'
            myconn.execute(query, (1212, requestPayloads[ApiKey.CUS_ID.value]))
            mydb.commit()

            return jsonify(ApiResponse(Status.SUCCESS.value, Messages.RESEND_OTP.value,
                                       dict()).__dict__), Status.SUCCESS.value
    except Exception as e:
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
