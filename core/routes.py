from typing import List

from fastapi import APIRouter, Body, Depends, File, Response, UploadFile

from core.schemas import (Customer_Pydantic, CustomerIn_Pydantic,
                          Device_Pydantic, DeviceIn, DeviceList,
                          Nomenclatura_Pydantic, NomenclaturaIn_Pydantic,
                          Order_Pydantic, OrderIn)
from core.service import (BaseService, CustomerService, DeviceService,
                          NomenclaturaService, OrderService)

router = APIRouter(prefix='', tags=['Venus', ])


def set_total_count(response: Response, total_count: int):
    response.headers.append('x-total-count', str(total_count))


@router.get('/devices', response_model=List[DeviceList])
async def get_devices(
    response: Response,
    limit: int = -1, page: int = 1,
    service: BaseService = Depends(DeviceService)
):
    devices, total_count = await service.get_all(limit, page)
    set_total_count(response, total_count)

    return await DeviceList.from_queryset(devices)


@router.get('/devices/{id}', response_model=Device_Pydantic)
async def get_device(id: int, service: BaseService = Depends(DeviceService)):
    return await Device_Pydantic.from_queryset_single(service.get(id))


@router.post('/devices', response_model=Device_Pydantic)
async def create_device(
    device: DeviceIn = Body(...),
    attachments: list[UploadFile] = File(...),
    service: BaseService = Depends(DeviceService)
):
    obj = await service.create(device, attachments)
    return await Device_Pydantic.from_tortoise_orm(obj)


@router.get('/customers', response_model=List[Customer_Pydantic])
async def get_customers(
    response: Response,
    limit: int = -1, page: int = 1,
    service: BaseService = Depends(CustomerService)
):
    customers, total_count = await service.get_all(limit, page)
    set_total_count(response, total_count)

    return await Customer_Pydantic.from_queryset(customers)


@router.get('/customers/{id}', response_model=Customer_Pydantic)
async def get_consumer(id: int, service: BaseService = Depends(CustomerService)):
    return await Customer_Pydantic.from_queryset_single(service.get(id))


@router.post('/customers', response_model=Customer_Pydantic)
async def create_customer(customer: CustomerIn_Pydantic,
                          service: BaseService = Depends(CustomerService)):
    obj = await service.create(customer)
    return await Customer_Pydantic.from_tortoise_orm(obj)


@router.get('/orders', response_model=List[Order_Pydantic])
async def get_orders(
    response: Response,
    limit: int = -1,
    page: int = 1,
    service: BaseService = Depends(OrderService)
):
    orders, total_count = await service.get_all(limit, page)
    set_total_count(response, total_count)
    return await Order_Pydantic.from_queryset(orders)


@router.get('/orders/{id}', response_model=Order_Pydantic)
async def get_order(id: int, service: BaseService = Depends(OrderService)):
    return await Order_Pydantic.from_queryset_single(service.get(id))


@router.post('/orders', response_model=Order_Pydantic)
async def create_order(order: OrderIn, service: BaseService = Depends(OrderService)):
    obj = await service.create(order)
    return await Order_Pydantic.from_tortoise_orm(obj)


@router.get('/nomenclatura', response_model=List[Nomenclatura_Pydantic])
async def get_nomenclatura(
    response: Response,
    limit: int = -1,
    page: int = 1,
    service: BaseService = Depends(NomenclaturaService)
):
    nomen, total_count = await service.get_all(limit, page)
    set_total_count(response, total_count)
    return await Nomenclatura_Pydantic.from_queryset(nomen)


@router.post('/nomenclatura', response_model=Nomenclatura_Pydantic)
async def create_nomenclatura(device: NomenclaturaIn_Pydantic,
                              service: BaseService = Depends(NomenclaturaService)):
    obj = await service.create(device)
    return await Nomenclatura_Pydantic.from_tortoise_orm(obj)
