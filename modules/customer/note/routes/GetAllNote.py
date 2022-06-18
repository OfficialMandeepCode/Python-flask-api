import jwt
from flask import Blueprint, jsonify, request, current_app

from ApiResponseHandler.ApiResponse import ApiResponse
from AuthToken.JWTToken import JWTToken
from Constant.ApiKey import ApiKey
from Constant.Messages import Messages
from Constant.SqlConstant import SqlConstant
from Constant.Status import Status
from DataModels.Customer.Notes.NoteDataClass import Note
from Database.DbConection import mydb
from Utils.Wrappers import CheckHeadersWrapper, CheckApiKeysWraaper
from DataModels.Customer.Notes.NoteAllList import NoteAll
allNote = Blueprint("allNote", __name__)

'''
Python Flask  API
Developed By : Mandeep Singh
'''

@allNote.route('allNote', methods=['GET'])
@CheckHeadersWrapper.isContentLanguageHeaderAdded
@CheckHeadersWrapper.isAccessTokenHeaderAdded
def AllNote():
    requestheaders = request.headers
    try:
        decodeUserData = JWTToken.decodeToken(requestheaders[ApiKey.ACCESS_TOKEN.value])
        print(decodeUserData)
        with mydb.cursor() as myconn:
            query = f'select * from {SqlConstant.TB_NOTE.value} where {SqlConstant.USER_ID.value} = %s'
            myconn.execute(query, (decodeUserData[ApiKey.CUS_ID.value]))
            mydb.commit()
            userNoteList = list()
            for item in myconn.fetchall():

                noteModel = Note(noteId=item[0], title=item[1], notebookText=item[2], isFavourite=item[3],
                                 isSecure=item[4], createdAt=item[5], lastUpdateAt=item[6])
                userNoteList.insert(len(userNoteList),noteModel.__dict__)
                notesList = NoteAll(len(userNoteList), userNoteList)

            current_app.logger.info(f'Response: {notesList.__dict__} \n on Request Url: {request.url}')
            return jsonify(ApiResponse(Status.SUCCESS.value, Messages.EXECUTION_SUCCESSFULLY.value,
                                       notesList.__dict__).__dict__), Status.SUCCESS.value

    except jwt.ExpiredSignatureError as err:
        print(f'Exception: {err}')
        current_app.logger.error(f'Errror: {err} on Request\n Url: {request.url}')
        return jsonify(ApiResponse(Status.UN_AUTHORISED.value, Messages.TOKEN_EXPIRED.value,
                                       dict()).__dict__), Status.UN_AUTHORISED.value
    except Exception as e:
        print(f'Exception: {e} ')
        current_app.logger.error(f'Errror: {e} on Request\n Url: {request.url}')
        return jsonify(ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value,
                                   dict()).__dict__), Status.ABORT.value
