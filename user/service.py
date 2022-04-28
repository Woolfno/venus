from pendulum import datetime
from tortoise.models import Model
from tortoise.queryset import QuerySetSingle
from tortoise.contrib.pydantic import PydanticModel
from pydantic import BaseModel
from user.models import User
from auth.utils import get_password_hash
from user.schemes import UserCreate


class BaseService:
    model: Model

    async def get_all(self, limit, page) -> tuple[QuerySetSingle, int]:
        total_count = await self.model.all().count()
        page = page if page > 0 else 1

        if limit < 0:
            data = self.model.all()
        else:
            data = self.model.all().limit(limit).offset(limit*(page-1))

        return (data, total_count)

    def get(self, id: int) -> QuerySetSingle:
        return self.model.get(id=id)

    async def create(self, data: BaseModel | PydanticModel, **kwargs) -> Model:
        return await self.model.create(**data.dict(exclude_unset=True))


class UserService(BaseService):
    model = User
    
    async def get_by_username(self, username:str) ->QuerySetSingle:
        return await self.model.get(username=username)
    
    async def create(self, data: UserCreate, **kwargs) -> Model:
        return await self.model.create(
            **data.dict(exclude_unset=True, exclude={'password'}), 
            password=get_password_hash(data.password))
        
    async def update_last_login(self, username:str):
        await self.model.filter(username=username).update(
            last_login=datetime.datetime.now())
        