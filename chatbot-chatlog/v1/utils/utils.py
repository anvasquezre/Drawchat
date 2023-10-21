from typing import Optional
import jwt
from jwt.exceptions import InvalidSignatureError

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.settings import settings
from pymongo import MongoClient

security = HTTPBearer()
API_KEY = settings.api.API_KEY
ALG = settings.api.ALG


async def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token,API_KEY,algorithms=[ALG],verify=True)
    except InvalidSignatureError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))

# Define a dependency to get the MongoDB collection
def get_client():
    host = settings.db.MONGO_CHATLOG_DB_HOST
    port = int(settings.db.MONGO_CHATLOG_DB_PORT)
    username = settings.db.MONGO_CHATLOG_DB_USERNAME
    password = settings.db.MONGO_CHATLOG_DB_PASSWORD
    path_pem = settings.db.MONGO_CHATLOG_DB_PEM_PATH
    try:
        # Establish the MongoDB connection and return the client
        client =MongoClient(
            host=host, 
            port=port, 
            username=username, 
            password=password, 
            tlsCAFile=path_pem, 
            replicaSet='rs0', 
            tls=True,
            retryWrites=False,
            readPreference='secondaryPreferred'
            )
        yield client
    finally:
        # Close the MongoDB connection when the request is finished
        client.close()