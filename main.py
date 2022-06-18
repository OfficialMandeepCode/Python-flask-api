import os
from multiprocessing import process

from flask import Flask, json, url_for
import logging
from logging.handlers import TimedRotatingFileHandler
from Utils.Wrappers.CheckHeadersWrapper import *
from modules.customer.authentication import AuthHome
from modules.customer.note import NoteHome
from Database.DbConection import mydb

# from Utils.Wrappers.CheckRequestMethodWrapper import *
"""
Python Flask  API
Developed By : Mandeep Singh
"""

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(AuthHome.authHome, url_prefix='/api/customer/')
app.register_blueprint(NoteHome.noteHome, url_prefix='/api/customer/')

with open('config.json', 'r') as config:
    params = json.load(config)["logger"]
    print(params)

logname = f"LogsBook/logs/{params['log_file']}.log"
logging.basicConfig(
    datefmt='%m/%d/%Y %I:%M:%S %p',
    format='[%(asctime)s] %(levelname)s %(name)s  %(message)s',
    level=logging.DEBUG,
    handlers=[TimedRotatingFileHandler(logname, when=params['when_midnight'], backupCount=params['backupCount'],
                                       interval=params['interval'])])

# app.logger.info(f'Firebase Admin SDK Project Id: {FirebaseHome().cred.project_id}')


@app.route('/')
# @isContentLanguageHeaderAdded
def home():
    app.logger.info(f'{Messages.EXECUTION_SUCCESSFULLY.value}\n Url: %s', request.url)
    print(f'Databse Name: {mydb.db}')
    return jsonify(ApiResponse(Status.SUCCESS, Messages.EXECUTION_SUCCESSFULLY.value,
                               dict()).__dict__), Status.SUCCESS.value


@app.errorhandler(400)
def error_handler(e):
    app.logger.warning(f'{Messages.SOME_WENT_WRONG.value}\n url: %s', request.url)
    return jsonify(
        ApiResponse(Status.ABORT.value, Messages.SOME_WENT_WRONG.value, dict()).__dict__), Status.ABORT.value


@app.errorhandler(500)
def error_internal_server(e):
    app.logger.warning(f'{Messages.INTERNAL_SERVER_ISSUE.value}\n url: %s', request.url)
    return jsonify(
        ApiResponse(Status.ABORT.value, Messages.INTERNAL_SERVER_ISSUE.value, dict()).__dict__), Status.ABORT.value


@app.errorhandler(404)
def resource_not_found(e):
    app.logger.warning(f'{Messages.NOT_FOUND_YOUR_REQUEST.value}\n url: %s', request.url)
    return jsonify(ApiResponse(Status.NOT_FOUND.value, Messages.NOT_FOUND_YOUR_REQUEST.value,
                               dict()).__dict__), Status.NOT_FOUND.value


@app.errorhandler(405)
def error_type_not_allowed(e):
    app.logger.warning(f'{Messages.TYPE_NOT_ALLOWED.value}\n url: %s', request.url)
    return jsonify(ApiResponse(Status.TYPE_NOT_ALLOWED.value, Messages.TYPE_NOT_ALLOWED.value,
                               dict()).__dict__), Status.TYPE_NOT_ALLOWED.value


@app.after_request
def after_response(response):
    return response

'''
Run App
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
