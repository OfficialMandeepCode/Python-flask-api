import pymysql
from flask import json
'''
Python Flask  API
Developed By : Mandeep Singh
'''
with open('config.json', 'r') as config:
    params = json.load(config)["database"]
    print(params)

mydb = pymysql.connect(host=params['host'], user=params['username'], password=params['password'], db=params['db_name'])
myDbConn = mydb.cursor()
