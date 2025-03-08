import uuid
from typing import List

from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Query, Session

from ..config.db import DbUtils
from ..exceptions.dao_exceptions import DataBaseException, DataAlreadyExistException, DataNotFoundException, \
    DataNotValidException
from ..schema.base import ListArgsSchema, ListFilterSchema, ListOrderSchema, ListKeySchema
from ..utils.converter.obj2dict import obj2dict


class BaseDao(object):
    Model = None

    def __init__(self, user_id=0):
        self.user_id = user_id
        self.db = DbUtils()

    def exists(self, id: str) -> bool:
        with Session(self.db.engine) as sess:
            return sess.query(self.Model).filter(self.Model.id == id).first() is not None

    def create(self, model: Model):
        try:
            if model.id is None or model.id == '':
                model.id = str(uuid.uuid4())
            self.db.sess.add(model)
            self.db.sess.flush()
            self.db.sess.commit()
            return True
        except IntegrityError as e:
            self.db.sess.rollback()
            # logger.error(f"Error: {e}")
            raise DataAlreadyExistException("Data already exists")


    def create_list(self, model_list: List[Model]):
        with Session(self.db.engine) as sess:
            try:
                for model in model_list:
                    if model.id is None or model.id == '':
                        model.id = str(uuid.uuid4())
                    sess.add(model)
                sess.commit()
                return True
            except IntegrityError:
                sess.rollback()
                # logger.error(f"Data list already exists: {model_list}")
                raise DataAlreadyExistException("Data already exists")

    def get(self, id: str) -> Model:
        filters = []
        with Session(self.db.engine) as sess:
            result = sess.query(self.Model).filter(self.Model.id == id, *filters).first()
            if not result:
                # logger.error(f"Data not found: {id}")
                raise DataNotFoundException("Data not found")
            return result

    def get_by_id_list(self, id_list: List[str]) -> List[Model]:
        with Session(self.db.engine) as sess:
            try:
                result = sess.query(self.Model).filter(self.Model.id.in_(id_list)).all()
                if not result:
                    # logger.error(f"Data not found: {id_list}")
                    raise DataNotFoundException("Data not found")
                return result
            except SQLAlchemyError as e:
                raise DataBaseException(f"Failed to retrieve the records: {e}")

    def update(self, model: Model):
        try:
            self.db.sess.merge(model)
            self.db.sess.flush()
            self.db.sess.commit()
            return True
        except SQLAlchemyError as e:
            self.db.sess.rollback()
            # logger.error(f"Failed to update the record: {e}")
            raise DataNotValidException("Invalid data provided")

    def update_list(self, model_list: List[Model]):
        with Session(self.db.engine) as sess:
            try:
                for model in model_list:
                    if not hasattr(model, 'id'):
                        # logger.error(f"Model {model} does not have an 'id' attribute")
                        # logger.error(f"Model {model} does not have an 'id' attribute")
                        raise ValueError("Model must have an 'id' attribute")
                    sess.merge(model)
                sess.commit()
                return True
            except SQLAlchemyError as e:
                sess.rollback()
                raise DataBaseException(e)

    def delete(self, model: Model):
        return self.delete_by_id(model.id)
        # try:
        #     sess.delete(self.Model).where(self.Model.id == model.id)
        #     sess.commit()
        #     return True
        # except SQLAlchemyError as e:
        #     sess.rollback()
        #     # You can raise a more specific exception based on the nature of the error
        #     raise DataBaseException(f"Failed to delete the record: {e}")

    def delete_by_id(self, id: str):
        with Session(self.db.engine) as sess:
            record = sess.query(self.Model).filter(self.Model.id == id).first()
            if not record:
                # logger.error(f"Data not found: {id}")
                raise DataNotFoundException("Data not found for deletion")

            sess.delete(record)
            sess.commit()
            return True

    def delete_by_id_list(self, id_list: List[str]):
        with Session(self.db.engine) as sess:
            try:
                sess.query(self.Model).filter(self.Model.id.in_(id_list)).delete(synchronize_session=False)
                sess.commit()
                return True
            except SQLAlchemyError as e:
                # logger.error(f"Failed to delete the records: {e}")
                sess.rollback()
                raise DataBaseException(f"Failed to delete the records: {e}")

    def get_list(self, args: ListArgsSchema, is_paging=True) -> List[Model]:
        if args is None:
            args = ListArgsSchema(
                page=1,
                size=10
            )
        filters = []
        filters.extend(self._handle_list_filters(args.filters))
        if args.keywords and hasattr(self.Model, 'search'):
            filters.append(and_(*[self.Model.search.like('%' + kw + '%') for kw in args.keywords.split(' ')]))
        with Session(self.db.engine) as sess:
            query = sess.query(self.Model).filter(*filters)
            count = query.count()
            orders = self._handle_list_orders(args.orders)
            obj_list = []
            if count == 0:
                # logger.error(f"Data not found in query: {args}")
                raise DataNotFoundException("Data not found")
            if args.start is None or args.start <= 0:
                obj_list = query.order_by(*orders).all()
            else:
                if is_paging:
                    obj_list = query.order_by(*orders).offset(args.get_offset()).limit(args.get_size()).all()
                else:
                    obj_list = query.order_by(*orders).all()
            return obj_list

    def _handle_list_filters(self, args_filters: List[ListFilterSchema]):

        filters = []

        if args_filters:
            for item in args_filters:
                if hasattr(self.Model, item.key):
                    attr = getattr(self.Model, item.key)
                    if item.condition == '=' or item.condition == '==':
                        filters.append(attr == item.value)
                    elif item.condition == '!=':
                        filters.append(attr != item.value)
                    elif item.condition == '<':
                        filters.append(attr < item.value)
                    elif item.condition == '>':
                        filters.append(attr > item.value)
                    elif item.condition == '<=':
                        filters.append(attr <= item.value)
                    elif item.condition == '>=':
                        filters.append(attr >= item.value)
                    elif item.condition == 'like':
                        filters.append(attr.like('%' + item.value + '%'))
                    elif item.condition == 'in':
                        filters.append(attr.in_(item.value.split(',')))
                    elif item.condition == '!in':
                        filters.append(~attr.in_(item.value.split(',')))
                    elif item.condition == 'null':
                        filters.append(attr.is_(None))
                    elif item.condition == '!null':
                        filters.append(~attr.isnot(None))
                else:
                    pass
                    # logger.error(f"Invalid filter key: {item.key}")

        return filters


    def _handle_list_orders(self, args_orders: ListOrderSchema):
        """
        处理list接口传入的排序条件
        :param args_orders: 传入排序条件
        :return: 转换后的sqlalchemy排序条件
        """
        orders = []

        if args_orders:
            for item in args_orders:
                if hasattr(self.Model, item.key):
                    attr = getattr(self.Model, item.key)

                    if item.condition == 'desc':
                        orders.append(attr.desc())
                    elif item.condition == 'asc':
                        orders.append(attr)
                    elif item.condition == 'rand':  # 随机排序
                        orders.append(func.rand())
                else:
                    pass
                    # logger.error(f"Invalid order key: {item.key}")
        else:
            if hasattr(self.Model, "id"):
                orders.append(self.Model.id.desc())

        return orders

    def _handle_list_orders_by_instance_variables(self, args_orders: ListOrderSchema):

        orders = []
        if args_orders:
            for item in args_orders:
                attr = getattr(self.Model, item.key)

                if item.condition == 'desc':
                    orders.append(attr.desc())
                elif item.condition == 'acs':
                    orders.append(attr)
                elif item.condition == 'rand':  # 随机排序
                    orders.append(func.rand())
        else:
            orders.append(self.Model.id.desc())

        return orders

    def _handle_list_keys(self, args_keys: ListKeySchema, obj_list: List):
        """
        处理list返回数据，根据传入参数keys进行过滤
        :param args_keys: 传入过滤字段
        :return: 转换后的list数据，数据转为dict类型
        """
        keys = []

        if args_keys:
            for item in args_keys:
                if hasattr(self.Model, item.key):
                    keys.append(item)

        resp_list = []

        for obj in obj_list:
            dict_1 = obj2dict(obj)

            # 判断：keys存在，不存在则返回所有字段
            if keys:
                dict_2 = {}
                for item in keys:
                    if item.rename:
                        dict_2[item.rename] = dict_1[item.key]
                    else:
                        dict_2[item.key] = dict_1[item.key]
            else:
                dict_2 = dict_1

            resp_list.append(dict_2)

        return resp_list

