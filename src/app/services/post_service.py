from fastapi import Depends

from app.dao.post_dao import PostDao
from app.models.post import Post
from app.schema.post import PostSchema
from app.services.base import BaseService


class PostService(BaseService):
    def __init__(self, dao: PostDao = Depends()):

        self.schema = PostSchema
        self.model = Post
        self.dao: PostDao = dao

        super().__init__()