
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schema.base import BaseObjSchema

class UserSchema(BaseObjSchema):
    id: Optional[str] = Field(None, examples=["550e8400-e29b-41d4-a716-446655440000"])
    name: str=Field(..., examples=["John"])
    email: str = Field(..., examples=["JohnDoe@c.c"])
    remark: Optional[str] = Field(None, examples=["Make America great again"])
    password: Optional[str] = Field(None, examples=["123455"])