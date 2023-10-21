from typing import Optional
import jwt
from jwt.exceptions import InvalidSignatureError

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.settings import settings
import uuid

security = HTTPBearer()
API_KEY = settings.api.SECRET
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


def generate_uuid():
    return str(uuid.uuid4())
