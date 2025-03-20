from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schema.base import BaseObjSchema


class PostSchema(BaseObjSchema):
    id: Optional[str] = Field(None, examples=["550e8400-e29b-41d4-a716-446655440000"])  # Unique post ID (UUID)
    poster_id: str=Field(..., examples=["123e4567-e89b-12d3-a456-426614174000"])  # User ID who posted the post
    poster_name: str = Field(..., examples=["JohnDoe"])  # Name of the person who posted
    num_likes: int = Field(0, examples=[100])  # Number of likes (not source of truth)
    post_time: Optional[datetime] = Field(None, examples=["2023-03-08T12:30:00"])  # Time when post was created
    title: str = Field(..., examples=["My First Blog Post"])  # Title of the post
    content: Optional[str] = Field(None, examples=["This is the content of the post."])  # Post content
