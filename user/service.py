from datetime import datetime

from auth.utils import get_password_hash
from base.service import BaseService
from tortoise.models import Model
from tortoise.queryset import QuerySetSingle

from user.models import User
from user.schemes import UserCreate


class UserService(BaseService):
    model = User

    async def get_by_username(self, username: str) -> QuerySetSingle:
        return await self.model.get(username=username)

    async def create(self, data: UserCreate, **kwargs) -> Model:
        return await self.model.create(
            **data.dict(exclude_unset=True, exclude={'password'}),
            password=get_password_hash(data.password))

    async def update_last_login(self, username: str):
        await self.model.filter(username=username).update(
            last_login=datetime.now())
