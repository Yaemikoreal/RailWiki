from pymongo import MongoClient
import db.db_settings as settings
import pymysql


def get_mongo_client():
    """获取MongoDB连接（单例模式）"""
    return MongoClient(
        host=settings.MONGO_DATABASES.get("MONGO_HOST"),
        port=settings.MONGO_DATABASES.get("MONGO_PORT"),
        username=settings.MONGO_DATABASES.get("MONGO_USER"),
        password=settings.MONGO_DATABASES.get("MONGO_PASS"),
        authSource=settings.MONGO_DATABASES.get("MONGO_AUTH_DB"),
        maxPoolSize=50  # 连接池参数
    )


def get_mysql_client():
    """获取MYSQL连接"""
    return pymysql.connect(
        host=settings.MYSQL_DATABASES.get("HOST"),
        user=settings.MYSQL_DATABASES.get("USER"),
        password=settings.MYSQL_DATABASES.get("PASSWORD"),
        database=settings.MYSQL_DATABASES.get("NAME"),
        charset="utf8mb4"
    )
