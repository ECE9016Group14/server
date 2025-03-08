from src.app.schema.base import CommRes
from src.app.utils.constants import ErrorType


class DataBaseException(Exception):
    def __init__(self, message="Database Access Error"):
        self.message = message
        super().__init__(self.message)
    def to_response(self,value):
        return CommRes.error(ErrorType.DATABASE,self.message,value)

class DataNotFoundException(DataBaseException):
    def __init__(self, message="Data Not Found"):
        self.message = message
        super().__init__(self.message)

class DataAlreadyExistException(DataBaseException):
    def __init__(self, message="Data Already Exist"):
        self.message = message
        super().__init__(self.message)

class DataNotValidException(DataBaseException):
    def __init__(self, message="Data Not Valid"):
        self.message = message
        super().__init__(self.message)

class DataNotUniqueException(DataBaseException):
    def __init__(self, message="Data Not Unique"):
        self.message = message
        super().__init__(self.message)

class QueryException(DataBaseException):
    def __init__(self, message="Query Error"):
        self.message = message
        super().__init__(self.message)


