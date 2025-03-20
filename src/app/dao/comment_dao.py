from app.dao.base import BaseDao
from app.models.comment import Comment


class CommentDao(BaseDao):
    def __init__(self):
        self.Model = Comment
        super().__init__()
