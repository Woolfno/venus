from typing import List
from fastapi import APIRouter
from models import  Device, DeviceInField, Customer, Order
from schemas import (
    Device_Pydantic, DeviceIn_Pydantic,
    DeviceInField_Pydantic, DeviceInFieldIn,
    Customer_Pydantic, CustomerIn_Pydantic,
    Order_Pydantic, OrderIn)


router = APIRouter(prefix='')


@router.get('/devices', response_model=List[Device_Pydantic])
async def get_devices():
    return await Device_Pydantic.from_queryset(Device.all())


@router.post('/devices', response_model=Device_Pydantic)
async def create_device(device: DeviceIn_Pydantic):
    obj = await Device.create(**device.dict())
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
async def create_order(order:OrderIn):
    obj = await Order.create(**order.dict(exclude_unset=True))
    return await Order_Pydantic.from_tortoise_orm(obj)

@router.get('/device_in_field', response_model=List[DeviceInField_Pydantic])
async def get_device_in_field():
    return await DeviceInField_Pydantic.from_queryset(DeviceInField.all())

@router.post('/device_in_field', response_model=DeviceInField_Pydantic)
async def create_device_in_field(device:DeviceInFieldIn):
    obj = await DeviceInField.create(**device.dict(exclude_unset=True))
    return await DeviceInField_Pydantic.from_tortoise_orm(obj)
