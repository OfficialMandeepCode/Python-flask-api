import enum

'''
Python Flask  API
Developed By : Mandeep Singh
'''
class ApiKey(enum.Enum):
    '''Common Keys'''

    ''' Customer keys '''
    CUS_NAME = "name"
    EMAIL_ID = "emailId"
    AUTH_TOKEN = "authToken"
    DEVICE_TOKEN = "deviceToken"
    PASSWORD = "password"
    PHONE_NUMBER = "phoneNumber"
    COUNTRY_CODE = "countryCode"
    LOCATION_LAT = "locationLat"
    LOCATION_LONG = "locationLong"
    CREATED_AT = "createdAt"
    CUS_ID = "cusId"
    OTP_CODE = "otpCode"
    SESSION_ID = "sessionId"
    IS_PHONE_VERIFIED = "isPhoneVerified"

    NOTE_ID = 'noteId'
    TITTLE = 'title'
    NOTEBOOK_TEXT = 'notebookText'
    IS_FAVOURITE = 'isFavourite'
    IS_SECURE = 'isSecure'


    ''' Header's '''
    CONTENT_TYPE = "content-Type"
    CONTENT_LANGUAGE = "content-language"
    ACCESS_TOKEN = "access-token"

    ''' JWT Token'''
    TOKEN_EXPIRE = "exp"
    ISSUE_AT = "iat"
