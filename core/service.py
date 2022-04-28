import aiofiles
from base.service import BaseService
from fastapi import File, UploadFile
from pydantic import BaseModel
from settings import settings
from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model

from core.models import Attach, Customer, Device, Nomenclatura, Order


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
