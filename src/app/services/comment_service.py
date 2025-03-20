from fastapi import Depends

from app.dao.comment_dao import CommentDao
from app.models.comment import Comment
from app.schema.comment import CommentSchema

from app.services.base import BaseService


class CommentService(BaseService):
    def __init__(self, dao: CommentDao = Depends()):

        self.schema = CommentSchema
        self.model = Comment
        self.dao: CommentDao = dao

        super().__init__()