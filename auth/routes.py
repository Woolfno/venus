from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from auth.securety import authenticate_user, create_access_token
from settings import settings
from auth.schemes import Token
from user.service import BaseService, UserService


router = APIRouter(prefix='/auth')


@router.post('/token', response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm=Depends(),
                service:BaseService=Depends(UserService)):
    user = await authenticate_user(form_data.username, form_data.password, service)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'},
                            )
    access_token_expires = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub':user.username},
                                       expires_delta=access_token_expires)
    return {'access_token':access_token, 'token_type':'bearer'}


        