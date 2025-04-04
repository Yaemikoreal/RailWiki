# 📁 test_connection.py
from db.db_utils import MySQLManager, MongoManager


def test_mysql_connection():
    try:
        conn = MySQLManager.get_conn()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 + 1 AS result")
            print("MySQL测试成功:", cursor.fetchone())
        conn.close()  # 重要：归还连接到池
    except Exception as e:
        print("MySQL连接失败:", e)


def test_mongo_connection():
    try:
        db = MongoManager.get_db()
        print("MongoDB测试成功:", db.command('ping'))
    except Exception as e:
        print("MongoDB连接失败:", e)


if __name__ == '__main__':
    test_mysql_connection()
    test_mongo_connection()
