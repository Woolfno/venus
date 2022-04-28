from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from settings import settings
from user.models import User
from user.service import BaseService, UserService

from auth.schemes import TokenData
from auth.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


async def authenticate_user(username: str, password: str,
                            service: UserService) -> User:
    user = await service.get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    await service.update_last_login(username)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                            algorithm=settings.JWT_ALGORITHM)
    return encode_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),
                           service: UserService = Depends(UserService)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not valide username or password',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await service.get_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user
