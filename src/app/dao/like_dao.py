from sqlalchemy.orm import Session

from app.dao.base import BaseDao
from app.exceptions.dao_exceptions import DataNotFoundException
from app.models.Like import Like


class LikeDao(BaseDao):
    def __init__(self):
        self.Model = Like
        super().__init__()

    def delete_like(self,user_id: str, post_id: str):
        with Session(self.db.engine) as sess:
            record = sess.query(self.Model).filter(self.Model.user_id==user_id).filter(self.Model.post_id==post_id).first()
            if not record:
                # logger.error(f"Data not found: {id}")
                raise DataNotFoundException("Data not found for deletion")

            sess.delete(record)
            sess.commit()
            return True
