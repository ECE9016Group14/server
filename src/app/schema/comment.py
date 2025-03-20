
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schema.base import BaseObjSchema
class CommentSchema(BaseObjSchema):
    id: Optional[str] = Field(None, examples=["550e8400-e29b-41d4-a716-446655440000"])  # Unique comment ID (UUID)
    poster_id: str = Field(..., examples=["123e4567-e89b-12d3-a456-426614174000"])  # User ID who posted the comment
    poster_name: str = Field(..., examples=["JohnDoe"])  # Name of the person who commented
    post_time: Optional[datetime] = Field(None, examples=["2023-03-08T12:30:00"])  # Time when comment was posted
    parent_post_id: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440001"])  # ID of the post being commented on
    content: str = Field(..., examples=["This is a comment content."])  # Content of the comment

class LikeSchema(BaseObjSchema):
    id: str = Field(None, examples=["1"],description="Useless field. Just add a random number")  # Unique like ID (UUID)
    user_id: str = Field(..., examples=["1"])  # User ID who liked the post
    post_id: str = Field(..., examples=["1"])  # ID of the post being liked