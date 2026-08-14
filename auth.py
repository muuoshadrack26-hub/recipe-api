from fastapi import Depends, HTTPException
from jwt import PyJWTError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timezone, timedelta
import jwt
from sqlmodel import select

from database import SessionDep
from model import User


pwd_context = PasswordHash.recommended()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY="899782a10a58ef6e81bf49c3d8d3fc9705cc97144443068dd3a085ffb1dea4e6"
ALGORITHM="HS256"


def create_access_token(data: dict):

    token = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=15)
    token.update({"exp": expire})
    encoded_jwt = jwt.encode(token, SECRET_KEY, algorithm=ALGORITHM)
    print(token)
    return  encoded_jwt

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except PyJWTError:

        raise HTTPException(401, "unauthorized")
    print(payload)

    user = session.exec(select(User).where(User.username == username)).first()

    if user is None:
        raise HTTPException(404, "user not found")

    return user