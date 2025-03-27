# src/app/models/user.py
import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.post import Base
import uuid
class User(Base):
    __tablename__ = 'Users'

    id: Mapped[str] = mapped_column('ID', String(36), primary_key=True,default=lambda: str(uuid.uuid4()))
    name:Mapped[str] = mapped_column('Name', String(50), nullable=False)
    remark: Mapped[str] = mapped_column('Remark', String(1000))
    create_time: Mapped[datetime.datetime] = mapped_column('CreateTime', DateTime, nullable=False, server_default=func.now())
    email: Mapped[str] = mapped_column('Email', String(500), nullable=False)
    password: Mapped[Optional[str]] = mapped_column('Password', String(500))