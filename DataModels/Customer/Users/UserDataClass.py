"""
Python Flask  API
Developed By : Mandeep Singh
"""
class User():
    cusId = ""
    name = ""
    emailID = ""
    countryCode = ""
    phoneNumber = ""
    deviceToken = ""
    authToken = ""
    otpCode = ""
    isPhoneVerified = ""

    def __init__(self, emailId, countryCode, phoneNumber, deviceToken, cusId, otpCode,authToken="", name="", isPhoneVerified = 0):
        self.cusId = cusId
        self.name = name
        self.emailID = emailId
        self.deviceToken = deviceToken
        self.authToken = authToken
        self.countryCode = countryCode
        self.phoneNumber = phoneNumber
        # self.otpCode = otpCode
        self.isPhoneVerified = isPhoneVerified

