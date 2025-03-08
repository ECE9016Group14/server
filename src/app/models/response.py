from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from enum import Enum


T = TypeVar('T')  # 泛型类型


class CommResCode(Enum):
    SUCCESS = 0
    FAIL = 1
    BadRequest = 400
    AuthFail = 401
    SystemError = 500
    NotFound = 404


class CommRes(BaseModel, Generic[T]):
    err_code: CommResCode = Field(default=CommResCode.SUCCESS, description="错误码,默认为:0")
    message: str = Field(default="success", description="响应消息,默认为:success")
    total: int | None = Field(default=None, description="数据总数，默认为空")
    # 响应数据，类型为泛型类型T，可以是任意类型
    data: T | None = None

    def __init__(self, msg: str = "success", errorcode=CommResCode.SUCCESS, data: T = None, total: int = None):
        super().__init__()
        self.err_code = errorcode
        self.message = msg
        self.data = data
        self.total = total

    def to_dict(self):
        return {"errorcode": self.err_code.value, "message": self.message, "data": self.data, "total": self.total}

    def error(self, errorcode, msg: str = "请求失败"):
        self.err_code = errorcode
        self.message = msg
        return self

    def AuthError(self):
        self.err_code = CommResCode.AuthFail
        self.message = "权限不足！"

    def SystemError(self, message: str = "系统错误"):
        self.err_code = CommResCode.AuthFail
        self.message = message
