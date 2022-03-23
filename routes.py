import aiofiles
from typing import List
from fastapi import APIRouter, Body, File, Form, UploadFile
from core.models import Device, Customer, Nomenclatura, Order, Attach
from core.schemas import (
    Device_Pydantic, DeviceIn, DeviceList,
    Nomenclatura_Pydantic, NomenclaturaIn_Pydantic,
    Customer_Pydantic, CustomerIn_Pydantic,
    Order_Pydantic, OrderIn)
from settings import settings


router = APIRouter(prefix='')


@router.get('/devices', response_model=List[DeviceList])
async def get_devices():
    return await DeviceList.from_queryset(Device.all())

async def save_file(prefix_name:str, file:File) ->str:
    path = settings.MEDIA_ROOT / ''.join((prefix_name, file.filename))
    async with aiofiles.open(path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    return path

@router.post('/devices', response_model=Device_Pydantic)
async def create_device(
    device: DeviceIn=Body(...), 
    attachments:list[UploadFile]=File(...)
):
    obj = await Device.create(**device.dict())
    for attach in attachments:
        path = await save_file(f'dev_id_{obj.id}_', attach)
        await Attach.create(device_id=obj.id, file=path)
        
    return await Device_Pydantic.from_tortoise_orm(obj)


@router.get('/customers', response_model=List[Customer_Pydantic])
async def get_customers():
    return await Customer_Pydantic.from_queryset(Customer.all())


@router.post('/customers', response_model=Customer_Pydantic)
async def create_customer(customer: CustomerIn_Pydantic):
    obj = await Customer.create(**customer.dict())
    return await Customer_Pydantic.from_tortoise_orm(obj)


@router.get('/orders', response_model=List[Order_Pydantic])
async def get_orders():
    return await Order_Pydantic.from_queryset(Order.all())


@router.post('/orders', response_model=Order_Pydantic)
async def create_order(order: OrderIn):
    obj = await Order.create(**order.dict(exclude_unset=True))
    return await Order_Pydantic.from_tortoise_orm(obj)


@router.get('/nomenclatura', response_model=List[Nomenclatura_Pydantic])
async def get_device_in_field():
    return await Nomenclatura_Pydantic.from_queryset(Nomenclatura.all())


@router.post('/nomenclatura', response_model=Nomenclatura_Pydantic)
async def create_device_in_field(device: NomenclaturaIn_Pydantic):
    obj = await Nomenclatura.create(**device.dict(exclude_unset=True))
    return await Nomenclatura_Pydantic.from_tortoise_orm(obj)
