from datetime import datetime
import aiofiles
from base.service import BaseService
from fastapi import File, HTTPException, UploadFile, status
from pydantic import BaseModel
from core.schemas import Order_Pydantic
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
    
    async def update(self, id: int, data: BaseModel | PydanticModel, **kwargs):
        # data.last_update_at = datetime.utcnow()
        r = await self.model.filter(id=id).update(
                                **data.dict(exclude_unset=True),
                                last_update_at = datetime.utcnow())        
        if r==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return await self.model.get(id=id)

class NomenclaturaService(BaseService):
    model = Nomenclatura
