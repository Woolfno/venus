from enum import Enum
from tortoise import  Tortoise, fields, models
from user.models import User


class BaseModel(models.Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class Nomenclatura(BaseModel):
    '''Справочник оборудования. Номенклатура'''

    monufacturer = fields.TextField()
    model = fields.TextField()

    def __str__(self) -> str:
        return f'{self.monufacturer} - {self.model}'


class Customer(BaseModel):
    '''Организация пользователь оборудования'''

    name = fields.TextField()
    address = fields.TextField()
    city = fields.TextField()

    def __str__(self) -> str:
        return f'"{self.name}" - {self.address}'
    
class Contact(BaseModel):
    '''Контакты организации'''
    name = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=128)
    email = fields.CharField(max_length=32)
    customer:fields.ForeignKeyRelation['Customer'] = fields.ForeignKeyField(
        'models.Customer', related_name='contact', 
        on_delete=fields.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return f'{self.name} - "{self.customer.name}"'

class Device(BaseModel):
    '''Конкретное оборудование'''
    
    class OwnerStatus(str, Enum):
        RENT = 'Аренда'
        MED_INST = 'ЛПУ'
        PORTNERS = 'Портнеры'

    serial_number = fields.TextField()
    customer = fields.ForeignKeyField(
        'models.Customer', related_name='device', on_delete=fields.RESTRICT)
    analyzer = fields.ForeignKeyField(
        'models.Nomenclatura', related_name='device', on_delete=fields.RESTRICT)
    year = fields.CharField(max_length=4)
    owner_status = fields.CharEnumField(OwnerStatus, description='Статус')
    comment = fields.TextField()

class Attach(BaseModel):
    device = fields.ForeignKeyField('models.Device', related_name='attachments', 
                                    on_delete=fields.CASCADE)
    file = fields.CharField(max_length=255)

class Order(BaseModel):
    '''Заявки'''

    class Status(str, Enum):
        OPEN = 'Открыта'
        CLOSE = 'Закрыта'
        IN_PROCESS = 'В работе'
        NEED_INFO = 'Нужна информация'
        
    device = fields.ForeignKeyField(
        'models.Device', on_delete=fields.RESTRICT)
    description = fields.TextField()
    create_at = fields.DatetimeField(auto_now_add=True)
    last_update_at = fields.DatetimeField(auto_now=True)
    status = fields.CharEnumField(Status, default=Status.OPEN)
    executor = fields.ForeignKeyField('models.User', related_name='orders', 
                                      on_delete=fields.SET_NULL, null=True)


Tortoise.init_models(['core.models'],'models')