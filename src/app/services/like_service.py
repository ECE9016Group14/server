from fastapi import Depends

from app.dao.like_dao import LikeDao
from app.models.Like import Like
from app.schema.comment import LikeSchema
from app.services.base import BaseService


class LikeService(BaseService):
    def __init__(self, dao: LikeDao = Depends()):

        self.schema = LikeSchema
        self.model = Like
        self.dao: LikeDao = dao

        super().__init__()
    def delete_like(self, user_id: str, post_id:str):
        return self.dao.delete_like(user_id, post_id)