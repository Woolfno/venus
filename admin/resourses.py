from typing import List

from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.resources import (Action, Field, Link, Model, Dropdown,
                                     ToolbarAction)
from fastapi_admin.widgets import displays, filters, inputs
from starlette.requests import Request

from admin.models import Admin
from models import Device, Customer, DeviceInField, Order


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
    class DevicesRecource(Model):
        label = 'Устройства'
        model = Device
        icon = 'ti ti-server'
        page_title = 'Список устройств'
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
        
        async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
            toolbar_actions = await super().get_toolbar_actions(request)
            toolbar_actions.append(
                ToolbarAction(
                    label='ToolbarAction',
                    icon='ti ti-toggle-left',
                    name='toolbar_action',
                    method=Method.PATCH,
                )
            )
            return toolbar_actions
        
        async def get_actions(self, request: Request) -> List[Action]:
            actions = await super().get_actions(request)
            switch_status = Action(
                label="Switch Status",
                icon="ti ti-toggle-left",
                name="switch_status",
                method=Method.PUT,
            )
            actions.append(switch_status)
            return actions

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

    class DeviceInFieldResource(Model):
        label = 'Оборудование в полях'
        icon = 'ti ti-signal'
        model = DeviceInField
        page_title = 'Список оборудования'
        fields = ['serial_number', 'customer', 'analyzer', 'owner_status']
        filters = [
            filters.Search(name='serial_number', label='Серийный номер', 
                           search_mode='contains'),
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
    resources = (DevicesRecource, CustomerResource, 
                 DeviceInFieldResource, OrderResource)
    
