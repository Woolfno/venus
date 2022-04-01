from tortoise.models import Model
from tortoise import Tortoise, fields
import datetime


class User(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    email = fields.CharField(max_length=200, default="", unique=True)
    avatar = fields.CharField(max_length=200, default="", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"
    
    
Tortoise.init_models(['user.models'], 'models')