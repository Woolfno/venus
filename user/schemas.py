import json
from pydantic import BaseModel
from user import models
from tortoise.contrib.pydantic import pydantic_model_creator

User = pydantic_model_creator(models.User, exclude=['password',], name="User")


class UserBase(BaseModel):
    password:str
    email:str


class AttachFileMixin:    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json
        
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserCreate(UserBase):
    username:str    
    

class UserUpdate(UserBase):
    pass