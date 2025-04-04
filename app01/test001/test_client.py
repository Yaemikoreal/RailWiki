from pymongo import MongoClient
import pymysql
import db.db_utils as db_utils


def test_mongo_connection():
    client = db_utils.get_mongo_client()
    # 测试连接
    try:
        print(client.server_info())  # 打印 MongoDB 服务器信息
        db = client["school"]
        print(db.list_collection_names())  # 打印集合列表
    except Exception as e:
        print("错误:", e)


def test_mysql_connection():
    try:
        connection = db_utils.get_mysql_client()
        print("MySQL 连接成功！")

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 + 1 AS result")
            result = cursor.fetchone()
            print(f"测试查询结果: {result}")

    except pymysql.MySQLError as e:
        print(f"连接失败: {e}")


if __name__ == '__main__':
    test_mysql_connection()
    test_mongo_connection()