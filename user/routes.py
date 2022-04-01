from collections import namedtuple
from tempfile import NamedTemporaryFile
from typing import IO
from PIL import Image
import aiofiles
import shutil
from fastapi import Depends, File, HTTPException, Request, UploadFile, Header
from starlette import status
from fastapi.routing import APIRouter
from settings import settings
from user import models
from user import schemas


router = APIRouter(prefix='/users', tags=['User',])

@router.get('/', response_model=list[schemas.User])
async def get_users():
    return await schemas.User.from_queryset(models.User.all())

# async def save_file(prefix_name: str, file: File) -> str:
#     path = settings.MEDIA_ROOT.joinpath('avatars',
#                                         ''.join((prefix_name, file.filename)))
#     async with aiofiles.open(path, 'wb') as f:
#         content = await file.read()
#         await f.write(content)
#     return path

async def save_file(prefix_name:str, file:UploadFile, file_size:int):
    real_file_size = 0
    tmp:IO = NamedTemporaryFile(delete=False)
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size>file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail='File too large')
        tmp.write(chunk)
    tmp.close()
    path = settings.MEDIA_ROOT.joinpath('avatars',
                                         ''.join((prefix_name, file.filename)))
    shutil.move(tmp.name, path)
    return path


def is_image(file_path:str)->bool:
    try:
        Image.open(file_path)
    except IOError:
        return False
    return True


async def valid_content_length(content_length: int = Header(..., lt=1_050_000)): #1MB
    return content_length


@router.post('/', response_model=schemas.User)
async def create_user(user:schemas.UserCreate):
    obj = await models.User.create(**user.dict(exclude_unset=True))
    return schemas.User.from_orm(obj)

@router.post('/{id}/avatar')
async def set_avatar(
    id:int,
    file:UploadFile=File(...),
    file_size:int=Depends(valid_content_length)
):
    path = await save_file(f'user_id_{id}', file, file_size)
    if not is_image(path):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='File is not image'
        )
    await models.User.filter(id=id).update(avatar=path)
    return {'message': 'ok'}

@router.put('/{id}', response_model=schemas.User)
async def update_user(id:int, user:schemas.UserUpdate):
    await models.User.filter(id=id).update(**user.dict(exclude_unset=True))
    obj = await models.User.get(id=id)
    return schemas.User.from_queryset_single(obj)