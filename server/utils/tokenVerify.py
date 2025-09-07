import os
import datetime
import jwt
from dotenv import load_dotenv

load_dotenv()  #load's jwt secret and algo

jwtSecret = os.getenv("JWT_SECRET")
jwtAlgo = os.getenv("JWT_ALGO")

if not jwtSecret or not jwtAlgo:
    print("Provide jwt data")


def createToken(userId: str, email: str, userName: str, expiresIn=3600):
    """Using this function a jwt token can be created"""
    payload = {
        "userId": userId,
        "email": email,
        "userName": userName,
        "exp": datetime.datetime.utcnow()+datetime.timedelta(seconds=expiresIn)
    }
    
    return jwt.encode(payload, jwtSecret, algorithm=jwtAlgo)


def decodeToken(token):
    """this function help decode jwt token"""
    
    try:
        return jwt.decode(token, jwtSecret, algorithms=[jwtAlgo])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
