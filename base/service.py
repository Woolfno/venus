from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySetSingle

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
