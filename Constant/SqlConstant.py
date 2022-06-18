from enum import Enum

'''
Python Flask  API
Developed By : Mandeep Singh
'''
class SqlConstant(Enum):
    '''
    User Table Keys
    Table Name: tb_user
    @author: Mandeep Singh
    '''
    TB_USER = 'tb_user'
    USER_ID = 'user_id'
    NAME = 'name'
    EMAIL_ID = 'emailId'
    PHONE_NUMBER = 'phoneNumber'
    DEVICE_TOKEN = 'deviceToken'
    AUTH_TOKEN = 'authToken'
    COUNTRY_CODE = 'countryCode'
    OTP_CODE = 'otpCode'
    IS_PHONE_VERIFIED = 'isPhoneVerified'

    '''
       Note Table Keys
       Table Name: tb_note
       @author: Mandeep Singh
       '''
    TB_NOTE = 'tb_note'
    NOTE_ID = 'noteId'
    TITTLE = 'title'
    NOTEBOOK_TEXT = 'notebookText'
    IS_FAVOURITE = 'isFavourite'
    IS_SECURE = 'isSecure'
    LAST_UPDATE_AT = 'lastUpdateAt'
    CREATED_AT = 'createdAt'
