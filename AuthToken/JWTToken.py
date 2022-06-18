from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app

'''
Python Flask  API
Developed By : Mandeep Singh
'''
class JWTToken:
    def generateToken(payload, key="secret", algorithm="HS384"):
        payload['iat'] = datetime.now(timezone.utc)
        payload['exp'] = (datetime.now(timezone.utc) + timedelta(days=2))

        token = jwt.encode(payload=payload
                           , key=key, algorithm=algorithm)
        current_app.logger.info(f'Auth Token {token} for\n Payload {payload}')
        return token

    def decodeToken(token, key="secret", algorithms="HS384"):
        decodeToken = jwt.decode(jwt=token, key=key, algorithms=algorithms)
        current_app.logger.info(f'Decode Auth Token {token} \n Payload {decodeToken}')
        return decodeToken
