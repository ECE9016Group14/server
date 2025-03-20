from sqlalchemy import String, Integer, DateTime, Text, func, BINARY, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime

from app.models.post import Base
class Like(Base):
    __tablename__ = 'Likes'

    user_id = mapped_column('UserID', String(36), primary_key=True, nullable=False)
    post_id = mapped_column('PostID', String(36), primary_key=True, nullable=False)