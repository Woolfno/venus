import shutil
from tempfile import NamedTemporaryFile
from typing import IO

from auth.securety import get_current_user
from auth.utils import get_password_hash
from fastapi import Depends, File, Header, HTTPException, UploadFile
from fastapi.routing import APIRouter
from PIL import Image
from settings import settings
from starlette import status

from user import models, schemes
from user.service import BaseService, UserService

router = APIRouter(prefix='/users', tags=['User', ])


@router.get("/me", response_model=schemes.User)
async def read_users_me(current_user: schemes.User = Depends(get_current_user)):
    return current_user


@router.get('/', response_model=list[schemes.User])
async def get_users():
    return await schemes.User.from_queryset(models.User.all())

# async def save_file(prefix_name: str, file: File) -> str:
#     path = settings.MEDIA_ROOT.joinpath('avatars',
#                                         ''.join((prefix_name, file.filename)))
#     async with aiofiles.open(path, 'wb') as f:
#         content = await file.read()
#         await f.write(content)
#     return path


async def save_file(prefix_name: str, file: UploadFile, file_size: int):
    real_file_size = 0
    tmp: IO = NamedTemporaryFile(delete=False)
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail='File too large')
        tmp.write(chunk)
    tmp.close()
    path = settings.MEDIA_ROOT.joinpath('avatars',
                                        ''.join((prefix_name, file.filename)))
    shutil.move(tmp.name, path)
    return path


def is_image(file_path: str) -> bool:
    try:
        Image.open(file_path)
    except IOError:
        return False
    return True


async def valid_content_length(content_length: int = Header(..., lt=1_050_000)):  # 1MB
    return content_length


@router.post('/', response_model=schemes.User)
async def create_user(user: schemes.UserCreate,
                      service: BaseService = Depends(UserService)
                      ):
    obj = await service.create(user)
    return schemes.User.from_orm(obj)


@router.post('/{id}/avatar')
async def set_avatar(
    id: int,
    file: UploadFile = File(...),
    file_size: int = Depends(valid_content_length)
):
    path = await save_file(f'user_id_{id}', file, file_size)
    if not is_image(path):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='File is not image'
        )
    await models.User.filter(id=id).update(avatar=path)
    return {'message': 'ok'}


@router.put('/', response_model=schemes.User)
async def update_user(user: schemes.UserUpdate,
                      current_user: models.User = Depends(get_current_user)):
    user.password = get_password_hash(user.password)
    await models.User.filter(id=current_user.id).update(**user.dict(exclude_unset=True))
    current_user = await models.User.get(id=current_user.id)
    return current_user
