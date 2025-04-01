from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .base import BaseDao
from ..exceptions.dao_exceptions import DataNotValidException
from ..models.user import User
class UserDao(BaseDao):
    def __init__(self):
        self.Model = User
        super().__init__()
    def update_remark(self, user_id:str,remaek:str):
        with Session(self.db.engine) as sess:
            user = sess.query(User).filter(User.id == user_id).first()
            user.remark = remaek
            sess.commit()
            return True
    def update(self, model: "Model"):
        try:
            existing = self.db.sess.get(self.Model, model.id)
            if not existing:
                raise DataNotValidException("Record not found")

            for attr, value in vars(model).items():
                if attr.startswith("_") or attr.startswith('create_time'):
                    continue
                if not value:
                    continue
                setattr(existing, attr, value)

            self.db.sess.flush()
            self.db.sess.commit()
            return True
        except SQLAlchemyError:
            self.db.sess.rollback()
            raise DataNotValidException("Invalid data provided")

    def get_user_by_email(self, email: str) -> User | None:
        with Session(self.db.engine) as sess:
            return sess.query(User).filter(User.email == email).first()

