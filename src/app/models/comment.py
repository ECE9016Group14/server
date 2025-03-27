from sqlalchemy import String, Integer, DateTime, Text, func, BINARY, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
import datetime

from app.models import Base


class Comment(Base):
    __tablename__ = 'Comments'

    id = mapped_column('ID',String(36), primary_key=True)
    poster_id = mapped_column('PosterID',String(36), nullable=False)
    poster_name = mapped_column('PosterName',String(50), nullable=False)
    post_time = mapped_column('PostTime',DateTime, nullable=False, default=func.current_timestamp())
    parent_post_id = mapped_column('ParentPostID',String(36), ForeignKey('Posts.ID', ondelete='CASCADE'), nullable=False)
    content = mapped_column('Content',String(5000), nullable=False)

    # Relationship definitions (optional but recommended)
    # poster = relationship("User", back_populates="comments")
    # post = relationship("Post", back_populates="comments")
