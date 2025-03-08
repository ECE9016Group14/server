from datetime import datetime
from typing import List, Dict, Optional, Any

from pydantic import BaseModel, Field

from src.app.utils.converter.json_encoders import JSONEncoders

class BaseObjSchema(BaseModel):
    class Config:
        json_encoders = JSONEncoders.json_encoders
        # orm_mode = True  # 为模型实例
        from_attributes = True

class BaseParameterSchema(BaseObjSchema):
    userId: Optional[str] = Field(None, examples=[""])


class PageSchema(BaseObjSchema):
    start: Optional[int] = Field(None, examples=[1])
    end: Optional[int] = Field(None, examples=[10])

    def get_offset(self):
        return self.start - 1

    def get_size(self):
        return self.end - self.start + 1

    def is_paging(self):
        if (self.start is not None) and self.start > 0 and self.end >= self.start:
            return True
        return False


class CommRes(BaseObjSchema):

    succ: bool = True
    message: str = 'SUCCESS'
    data: Optional[Any] = None
    total: Optional[int] = None

    @staticmethod
    def success(data, message='SUCCESS'):
        res: CommRes = CommRes()
        res.succ = True
        res.message = message
        res.data = data
        res.total = len(data) if isinstance(data, list) else 1
        return res

    @staticmethod
    def success_count(data: Any, count: int):
        res: CommRes = CommRes()
        res.succ = True
        res.message = 'SUCCESS'
        res.data = data
        res.total = count
        return res

    @staticmethod
    def error(error_type: str, message: str, value=""):
        res: CommRes = CommRes()
        res.succ = False
        res.message = f"{error_type}:{message} {value}"
        res.total = 0
        return res





class ResponseIdSchema(CommRes):

    id: int = 0  # 返回id


class ResponseDetailSchema(CommRes):

    detail: dict = None  # 返回详情


class ResponseListSchema(CommRes):

    page: int = 0  # 当前页码
    size: int = 0  # 每页大小
    count: int = 0  # 数据总条数
    page_count: int = 0  # 总页数
    list: List[Dict] = None  # 数据list


class ListFilterSchema(BaseModel):

    key: str  # 字段名
    condition: str  # 过滤条件
    value: Any  # 条件值，如condition为in或!in时，value为用“,”分割的多值得字符串


class OrderConditionSchema(BaseObjSchema):
    order_field: Optional[str] = None
    is_desc: Optional[bool] = False

    def need_customized_order(self):
        return self.order_field is not None and len(self.order_field) > 0

    def get_order_filed(self, model_class: Any):
        if self.need_customized_order():
            if hasattr(model_class, self.order_field):
                attr = getattr(model_class, self.order_field)
                if self.is_desc is None or self.is_desc == False:
                    return attr
                else:
                    return attr.desc()
        from fastapi.exceptions import RequestValidationError
        raise RequestValidationError(f"model_class:{model_class} has no field:{self.order_field}")


class ListOrderSchema(BaseModel):

    key: str
    condition: str


class ListKeySchema(BaseModel):

    key: str
    rename: str = None


class ListArgsSchema(PageSchema):

    keywords: Optional[str] = None  # 关键字，用于模糊、分词搜索
    filters: Optional[List[ListFilterSchema]] = None  # 过滤条件
    orders: Optional[List[ListOrderSchema]] = None  # 排序条件
    keys: Optional[List[ListKeySchema]] = None  # 字段条件




class FileBaseSchema(BaseObjSchema):
    id: int
    name: str
    suffix: str


class InfoSchema(BaseObjSchema):

    id: int = None
    parent_id: int = None
    type: int = None
    sort: int = None
    status: int = None
    code: str = None
    name: str = None
    label: str = None
    logo: str = None
    url: str = None
    info: str = None
    remark: str = None


class DetailSchema(InfoSchema):

    created_time: datetime
    updated_time: datetime
