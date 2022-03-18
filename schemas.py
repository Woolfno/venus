from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from pydantic import BaseModel
from models import Device, Customer, DeviceInField, Order


Device_Pydantic = pydantic_model_creator(Device, name="Device")
DeviceIn_Pydantic = pydantic_model_creator(
    Device, exclude_readonly=True, name='DeviceIn')
Customer_Pydantic = pydantic_model_creator(Customer, name='Customer')
CustomerIn_Pydantic = pydantic_model_creator(
    Customer, exclude_readonly=True, name='CustomerIn')
DeviceInField_Pydantic = pydantic_model_creator(
    DeviceInField, name='DeviceInField')

class DeviceInFieldIn(PydanticModel):
    serial_number: str
    customer_id: int
    analyzer_id: int
    owner_status:str

Order_Pydantic = pydantic_model_creator(Order, name='Order')

class OrderIn(BaseModel):
    device_id: int
    description: str
    status: str
