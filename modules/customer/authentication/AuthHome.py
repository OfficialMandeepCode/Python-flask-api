from flask import Blueprint, jsonify, request,current_app
from ApiResponseHandler.ApiResponse import ApiResponse
from Constant.Messages import Messages
from Constant.Status import Status
from .routes.OnBoard import onBoard
from .routes.VerifyOTP import verifyOtp
from .routes.ResendOtp import resendOtp
from .routes.UpdateProfile import updateProfile
'''
Python Flask  API
Developed By : Mandeep Singh
'''

#/api/customer/auth
authHome = Blueprint("authHome", __name__)

authHome.register_blueprint(onBoard, url_prefix='/auth')
authHome.register_blueprint(verifyOtp, url_prefix='/auth')
authHome.register_blueprint(resendOtp, url_prefix='/auth')
authHome.register_blueprint(updateProfile, url_prefix='/auth')

@authHome.route('auth')
def auth_Home():
    current_app.logger.info(f'{Messages.WELCOME_AUTH_HOME.value}\n Url: %s', request.url)
    return jsonify(ApiResponse(Status.SUCCESS.value, Messages.WELCOME_AUTH_HOME.value,
                               dict()).__dict__), Status.SUCCESS.value
