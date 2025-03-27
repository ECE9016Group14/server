from sqlalchemy import String, Integer, DateTime, Text, func, BINARY
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import datetime

from app.models import Base


class Post(Base):
    __tablename__ = 'Posts'

    id: Mapped[str] = mapped_column('ID', String(36), primary_key=True)
    poster_id:Mapped[str] = mapped_column('PosterID', String(36), nullable=True)
    poster_name: Mapped[str] = mapped_column('PosterName', String(50), nullable=False)
    num_likes: Mapped[int] = mapped_column('NumLikes', Integer, nullable=False, comment="Needs to be recomputed occasionally by the server; it is not the source of truth")
    post_time: Mapped[datetime.datetime] = mapped_column('PostTime', DateTime, nullable=False, server_default=func.now())
    title: Mapped[str] = mapped_column('Title', String(100), nullable=False)
    content: Mapped[str | None] = mapped_column('Content', Text)  # Allows NULL by default