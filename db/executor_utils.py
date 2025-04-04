from typing import Optional, Union, List, Dict
from db.db_utils import MySQLManager, MongoManager


class MySQLExecutor:
    """
    MySQL 纯 SQL 执行器
    使用示例：
        result = MySQLExecutor.execute(
            "SELECT * FROM users WHERE id = %s",
            params=(1,),
            fetch_one=True
        )
    """

    @staticmethod
    def execute(
            sql: str,
            params: Optional[Union[tuple, dict]] = None,
            fetch_one: bool = False,
            fetch_all: bool = False,
            commit: bool = False
    ) -> Union[int, Dict, List[Dict], None]:
        """
        执行 SQL 语句
        :param sql: SQL 字符串
        :param params: 参数（元组或字典）
        :param fetch_one: 是否返回单条记录
        :param fetch_all: 是否返回所有记录
        :param commit: 是否提交事务（用于 INSERT/UPDATE/DELETE）
        :return: 查询结果或影响行数
        """
        with MySQLManager.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())

                if commit:
                    conn.commit()
                    return cursor.rowcount  # 返回影响行数

                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()
                return None


class MongoDBExecutor:
    """
    MongoDB 查询执行器
    使用示例：
        result = MongoDBExecutor.execute(
            "users",
            query={"age": {"$gt": 20}},
            operation="find"
        )
    """
    _client = None

    @staticmethod
    def execute(
            collection: str,
            operation: str,
            query: Optional[Dict] = None,
            update: Optional[Dict] = None,
            projection: Optional[Dict] = None,
            limit: int = 0
    ) -> Union[Dict, List[Dict], int, None]:
        """
        执行 MongoDB 操作
        :param collection: 集合名
        :param operation: 操作类型（find/find_one/insert/update/delete/count）
        :param query: 查询条件
        :param update: 更新数据（用于 update 操作）
        :param projection: 返回字段投影
        :param limit: 结果限制
        :return: 操作结果
        """
        db = MongoManager.get_db()
        col = db[collection]
        query = query or {}

        # 操作路由
        if operation == "find":
            return list(col.find(query, projection).limit(limit))
        elif operation == "find_one":
            return col.find_one(query, projection)
        elif operation == "insert":
            return col.insert_one(query).inserted_id
        elif operation == "update":
            result = col.update_many(query, update)
            return result.modified_count
        elif operation == "delete":
            result = col.delete_many(query)
            return result.deleted_count
        elif operation == "count":
            return col.count_documents(query)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
