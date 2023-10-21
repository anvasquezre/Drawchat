from typing import Optional
import jwt
from jwt.exceptions import InvalidSignatureError

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.settings import settings
import qdrant_client


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
    host = settings.qdrant.QDRANT_HOST
    port = int(settings.qdrant.QDRANT_PORT)
    https = settings.qdrant.QDRANT_USE_HTTPS
    grpc_port = int(settings.qdrant.QDRANT_GRPC_PORT)
    try:
        # Establish the MongoDB connection and return the client
        client = qdrant_client.QdrantClient(host=host,
                                            port=port, 
                                            prefer_grpc=True,
                                            https=https, 
                                            grpc_port=grpc_port
                                            )
        client.get_collections()
        yield client
    finally:
        # Close the MongoDB connection when the request is finished
        client.close()