from database.db import Base
from sqlalchemy import Column, String, Uuid,Enum, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

from models.user_models import UserRole, UserStatus

class User(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword", 
            }
        }
    )

class UserCreate(BaseModel):
    email: str
    password: str
    role: str | None = "USER"
    
class UserSchema(BaseModel):
    id: str
    email: str
    role: str
    status: str

    model_config = {
        "from_attributes": True,
        "use_enum_values": True 
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None 