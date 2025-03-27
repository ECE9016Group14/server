from typing import List, Type

from pydantic import BaseModel

from ..schema.base import ListArgsSchema


class BaseService(object):
    """Base(基础)服务，用于被继承.

    CRUD基础服务类，拥有基本方法，可直接继承使用

    Attributes:
        auth_data: 认证数据，包括用户、权限等
        user_id: 当前操作用户id
        event_dao: 业务事件dao
        dao: 当前业务数据处理类
    """

    auth_data: dict = {}
    user_id: str = 'qqq'

    dao = None
    schema = None
    model = None

    def __init__(self, userId: str = 0, auth_data: dict = {}):
        """Service初始化."""

        self.user_id = userId
        self.auth_data = auth_data

    def get(self, id: str) -> schema:
        return self.model2schema(self.dao.get(id), self.schema)

    def get_list(self, args: ListArgsSchema, is_paging=True) -> List[schema]:
        return self.model_list2schema_list(self.dao.get_list(args, is_paging), self.schema)

    def create(self, schema) -> schema:
        model = self.model()
        self.set_model_by_schema(schema, model)
        self.dao.create(model)
        return self.model2schema(model, self.schema)

    def update(self, schema):
        model = self.dao.get(schema.id)
        if not model:
            return None
        self.set_model_by_schema(schema, model)
        self.dao.update(model)
        return self.model2schema(model, self.schema)

    def update_list(self, schema_list: List[schema]):
        model_list = []
        model_list = self.schema_list2model_list(schema_list, self.model)
        self.dao.update_list(model_list)
        return True

    def delete(self, id: str) -> bool:
        model = self.dao.get(id)
        if not model:
            return None
        self.dao.delete(model)
        return True

    @staticmethod
    def model2schema(orm_model, schema_class: Type[BaseModel]) -> schema:
        return None if orm_model is None else schema_class.from_orm(orm_model)

    @staticmethod
    def model_list2schema_list(orm_model_list: List, schema_class: Type[BaseModel]) -> List[schema]:
        return [schema_class.from_orm(orm_model) for orm_model in orm_model_list]

    @staticmethod
    def schema_list2model_list(schema_list: List[schema], model) -> List[BaseModel]:
        model_list: List[model] = []
        for schema_item in schema_list:
            model_item = model()
            BaseService.set_model_by_schema(schema_item, model_item)
            model_list.append(model_item)
        return model_list

    @staticmethod
    def set_model_by_schema(schema, model):

        for (key, value) in schema:
            setattr(model, key, value)

        if hasattr(model, 'search'):
            model.search = model.name
