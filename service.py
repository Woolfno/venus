import aiofiles
from fastapi import File, UploadFile
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model
from tortoise.queryset import QuerySetSingle

from core.models import Attach, Customer, Device, Nomenclatura, Order
from settings import settings


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


class DeviceService(BaseService):
    model = Device

    async def __save_file(self, prefix_name: str, file: File) -> str:
        path = settings.MEDIA_ROOT / ''.join((prefix_name, file.filename))
        async with aiofiles.open(path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        return path

    async def create(self,
                     device: BaseModel | PydanticModel,
                     attachments: list[UploadFile] = File(...)
                    ) -> Model:
        obj = await Device.create(**device.dict())

        for attach in attachments:
            path = await self.__save_file(f'dev_id_{obj.id}_', attach)
            await Attach.create(device_id=obj.id, file=path)

        return obj


class CustomerService(BaseService):
    model = Customer


class OrderService(BaseService):
    model = Order
        
   
class NomenclaturaService(BaseService):
    model = Nomenclatura
