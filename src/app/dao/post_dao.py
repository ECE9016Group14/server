from app.dao.base import BaseDao
from app.models.post import Post


class PostDao(BaseDao):
    def __init__(self):
        self.Model = Post
        super().__init__()
