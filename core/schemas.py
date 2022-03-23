import json
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from pydantic import BaseModel
from core.models import Device, Customer, Order, Contact, Nomenclatura


Nomenclatura_Pydantic = pydantic_model_creator(Nomenclatura, name='Nomenclatura')
NomenclaturaIn_Pydantic = pydantic_model_creator(Nomenclatura, name='NomenclaturaIn', exclude_readonly=True)
Customer_Pydantic = pydantic_model_creator(Customer, name='Customer')
CustomerIn_Pydantic = pydantic_model_creator(
    Customer, exclude_readonly=True, name='CustomerIn')

Device_Pydantic = pydantic_model_creator(Device, name="Device")
DeviceList = pydantic_model_creator(Device, name='DeviceList', exclude=('attachments',))
class DeviceIn (BaseModel):
    serial_number: str
    customer_id: int
    analyzer_id: int
    year: str
    comment:str
    owner_status:str
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json
        
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

Order_Pydantic = pydantic_model_creator(Order, name='Order')

class OrderIn(BaseModel):
    device_id: int
    description: str
    status: str


class Simple(BaseModel):
    name:str