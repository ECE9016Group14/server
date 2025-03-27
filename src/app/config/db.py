import os
from typing import List

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session



class DbConfig(BaseSettings):
    """
    DbConfig DB配置类
    :version: 0.1
    """
    driver: str = os.getenv('DB_DRIVER', 'mysql+pymysql')
    host: str = os.getenv('DB_HOST', '35.226.3.0')
    port: str = os.getenv('DB_PORT', '3306')
    uname: str = os.getenv('DB_USERNAME', 'root')
    password: str = os.getenv('DB_PASSWORD', 'admin')
    database: str = os.getenv('DB_DATABASE', 'my_database')
    charset: str = os.getenv('DB_CHARSET', 'utf8')
    table_name_prefix: str = os.getenv('DB_TABLE_NAME_PREFIX', '')
    echo: bool = os.getenv('DB_ECHO', True)
    pool_size: int = os.getenv('DB_POOL_SIZE', 100)
    max_overflow: int = os.getenv('DB_MAX_OVERFLOW', 100)
    pool_recycle: int = os.getenv('DB_POOL_RECYCLE', 60)

    def get_url(self):
        config = [
            self.driver,
            '://',
            self.uname,
            ':',
            self.password.replace("@", "%40"),
            '@',
            self.host,
            ':',
            self.port,
            '/',
            self.database,
            '?charset=',
            self.charset,
        ]
        connection_str = ''.join(config)
        # return connection_str

        # return 'mssql+pymssql://em:Teld%40teld.cn@mgec.teld.cc:9040/TeldEM?charset=utf8'
        print(f'connect to db: {connection_str}')
        return connection_str


class DbUtils(object):
    """
    DbUtils DB工具类
    :version: 0.1
    """
    engine: Engine = None
    sess: Session = None
    default_config: DbConfig = DbConfig()

    def __init__(self, config: DbConfig = None):
        if not config:
            config = self.default_config
        self.engine, self.sess = self._create_scoped_session(config)

    def __del__(self):
        self.sess.close()

    @staticmethod
    def _create_scoped_session(config: DbConfig):
        engine = create_engine(
            config.get_url(),
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_recycle=config.pool_recycle,
            echo=config.echo
        )

        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        return engine, scoped_session(session_factory)

    # 根据文件获取SQL文件
    @staticmethod
    def get_sql_by_file(file_path, params={}):
        sql = DbUtils._get_file(file_path)
        return sql.format(**params)

    # 获取SQL文件
    @staticmethod
    def _get_file(file_path):
        with open('app/sql/' + file_path, 'r', encoding='utf-8') as f:
            return f.read()
