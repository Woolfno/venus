from typing import List

from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.resources import (Action, Field, Link, Model, Field,
                                     Dropdown, ToolbarAction)
from fastapi_admin.widgets import displays, filters, inputs
from fastapi_admin.file_upload import FileUpload
from starlette.requests import Request

from admin.models import Admin
from core.models import Device, Customer, Order, Contact, Nomenclatura
from settings import settings


upload = FileUpload(uploads_dir=settings.BASE_DIR/'upload')

@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "admin model"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        "created_at",
    ]

    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return []

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)

    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []

@app.register
class Content(Dropdown):    
    class NomenclaturaRecource(Model):
        label = 'Номенклатура'
        model = Nomenclatura
        icon = 'ti ti-server'
        page_title = 'Справочник оборудования'
        fields = ['monufacturer', 'model',]
        filters = [
            filters.Search(
                name='monufacturer', label='Производитель', 
                search_mode='contains'
            ),
            filters.Search(
                name='model', label='Модель', search_mode='contains'
            ),
        ]

    class ContactResource(Model):
        label = 'Контакты'
        icon = ''
        model = Contact
        page_title = 'Список контактов'
        fields = ['name', 'phone_number', 'email', 'customer']
        filters = [
            filters.Search(name='name', label='ФИО', search_mode='contains'),
            filters.Search(name='email', label='email', search_mode='contains'),
        ]
    
    class CustomerResource(Model):
        label = 'Контрагенты'
        icon = 'fas fa-address-card'
        model = Customer
        page_title = 'Список контрагентов'
        fields = ['name', 'address', 'city']
        filters = [
            filters.Search(name='name', label='Название', search_mode='contains'),
            filters.Search(name='city', label='Город', search_mode='contains'),
        ]

    class DeviceResource(Model):
        label = 'Оборудование'
        icon = 'ti ti-signal'
        model = Device
        page_title = 'Список оборудования'
        fields = ['serial_number', 'customer', 'analyzer', 
                  'owner_status', 'year', 'comment', 
                  Field(
                      name='file',
                      label='file',                      
                      input_=inputs.Image(null=True, upload=upload)
                  ),
                ]
        filters = [
            filters.Search(name='serial_number', label='Серийный номер', 
                           search_mode='contains'),
            filters.Search(name='year', label='Год выпуска', 
                           search_mode='equal'),
        ]

    class OrderResource(Model):
        label = 'Заказы'
        icon = 'fas fa-clipboard'
        model = Order
        page_title = 'Список заявок'
        fields = ['device', 'description', 'create_at', 
                    'last_update_at', 'status']    
        filters = [
            filters.ForeignKey(Device, name='device', label='Устройство'),
            filters.Enum(enum=Order.Status, enum_type=str, 
                         name='status', label='Статус'),
            filters.Date(name='create_at', label='Дата создания'),            
        ]
                
    
    label = 'Контент'
    icon = "fas fa-bars"
    resources = (NomenclaturaRecource, CustomerResource, ContactResource,
                 DeviceResource, OrderResource)
    
