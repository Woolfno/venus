from enum import Enum, IntEnum
from tortoise import Tortoise, fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class Device(BaseModel):
    '''Оборудование'''

    monufacturer = fields.TextField()
    model = fields.TextField()

    def __str__(self) -> str:
        return f'{self.monufacturer} - {self.model}'


class Customer(BaseModel):
    '''Конечный пользователь оборудования'''

    name = fields.TextField()
    address = fields.TextField()
    city = fields.TextField()

    def __str__(self) -> str:
        return f'"{self.name}" - {self.address}'

class DeviceInField(BaseModel):
    '''Оборудование в полях'''

    serial_number = fields.TextField()
    customer = fields.ForeignKeyField(
        'models.Customer', related_name='in_field', on_delete=fields.RESTRICT)
    analyzer = fields.ForeignKeyField(
        'models.Device', related_name='in_field', on_delete=fields.RESTRICT)
    owner_status = fields.TextField()
    

class Order(BaseModel):
    '''Заявки'''

    class Status(str, Enum):
        OPEN = 'Открыта'
        CLOSE = 'Закрыта'
        IN_PROCESS = 'В работе'
        NEED_INFO = 'Нужна информация'
        
    device = fields.ForeignKeyField(
        'models.DeviceInField', on_delete=fields.RESTRICT)
    description = fields.TextField()
    create_at = fields.DatetimeField(auto_now_add=True)
    last_update_at = fields.DatetimeField(auto_now=True)
    status = fields.CharEnumField(Status, default=Status.OPEN)
    

Tortoise.init_models(['models'],'models')