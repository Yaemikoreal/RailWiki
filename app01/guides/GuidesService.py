import app01.tools.CalculateTools as tools
from db.executor_utils import MySQLExecutor
import logging

logger = logging.getLogger(__name__)  # 自动继承全局配置

"""
光锥仪器相关数据库查询操作函数
"""


class GuidesService:
    @classmethod
    def get_light_cone(cls):
        """
        获取光锥整体信息
        :return:
        """
        try:
            query_sql = """
                  SELECT
                       id,
                       name,
                       paths
                  FROM
                      light_cone
                  """
            result = MySQLExecutor.execute(
                query_sql,
                fetch_all=True
            )
            keys = [
                "id", "name", "paths"
            ]
            # 结果整合为list
            result_lt = [tools.tuple_to_dict(keys=keys, data=row) for row in result]
            if not result_lt:  # 处理空结果
                return None
            return result_lt
        except Exception as e:
            logger.error(f"适配光锥信息查询出错: {str(e)}")
            return None
