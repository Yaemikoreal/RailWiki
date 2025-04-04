from pymongo import MongoClient
import db.db_settings as settings
import pymysql
from dbutils.pooled_db import PooledDB


class MongoManager:
    _client = None

    @classmethod
    def get_db(cls):
        if not cls._client:
            cls._client = MongoClient(
                host=settings.MONGO_DATABASES.get("MONGO_HOST"),
                port=settings.MONGO_DATABASES.get("MONGO_PORT"),
                username=settings.MONGO_DATABASES.get("MONGO_USER"),
                password=settings.MONGO_DATABASES.get("MONGO_PASS"),
                authSource=settings.MONGO_DATABASES.get("MONGO_AUTH_DB"),
                maxPoolSize=50  # 连接池参数
            )
        return cls._client[settings.MONGO_DATABASES['MONGO_DB_NAME']]


class MySQLManager:
    _pool = None

    @classmethod
    def get_conn(cls):
        if not cls._pool:
            mysql_config = {
                'host': settings.MYSQL_DATABASES['HOST'],
                'port': settings.MYSQL_DATABASES['PORT'],
                'user': settings.MYSQL_DATABASES['USER'],
                'password': settings.MYSQL_DATABASES['PASSWORD'],
                'db': settings.MYSQL_DATABASES['NAME'],
                'charset': 'utf8mb4'
            }
            # 创建连接池
            cls._pool = PooledDB(
                creator=pymysql,
                mincached=5,
                maxconnections=50,
                blocking=True,  # 连接池满时等待而非报错
                ping=1,  # 每次取连接时检查健康状态
                **mysql_config
            )
        return cls._pool.connection()

