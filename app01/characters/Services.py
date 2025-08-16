import app01.tools.CalculateTools as tools
from db.executor_utils import MySQLExecutor
import logging

logger = logging.getLogger(__name__)  # 自动继承全局配置

"""
角色相关数据库查询操作函数
"""


class CharacterService:
    @classmethod
    def get_character_msg(cls, char_id):
        """
        获取单个角色信息并返回角色信息字典
        :param char_id: 角色ID
        :return:
        """
        try:
            query_sql = """
                    SELECT
                        id,
                        NAME,
                        element,
                        path,
                        rarity,
                        position,
                        description,
                        release_date
                    FROM
                        characters
                    WHERE
                        id = %s
                """
            result = MySQLExecutor.execute(
                query_sql,
                params=(char_id,),
                fetch_one=True
            )
            if not result:  # 处理空结果
                return None
            keys = [
                "id", "name", "element",
                "path", "rarity", "position",
                "description", "release_date",
                # "character_image_1", "character_image_2", "character_image_3"
            ]
            character_dt = dict(zip(keys, result))
            if character_dt['release_date']:
                character_dt['release_date'] = character_dt.get('release_date').strftime("%Y/%m/%d")
            else:
                character_dt['release_date'] = "暂无"
            return character_dt
        except Exception as e:
            logger.error(f"角色查询出错: {str(e)}")

    @classmethod
    def get_characters_list(cls, data_dt):
        """
        动态条件查询角色列表
        :param data_dt: 包含过滤条件的字典（elements/paths/rarities）
        :return: 结果列表或None（查询失败时）
        """
        # 动态构建WHERE条件
        conditions = []
        params = []

        # 元素过滤（支持多选）
        if elements := data_dt.get("elements"):
            if isinstance(elements, str):
                elements = [elements]
            placeholders = ",".join(["%s"] * len(elements))
            conditions.append(f"element IN ({placeholders})")
            params.extend(elements)

        # 命途过滤（支持多选）
        if paths := data_dt.get("paths"):
            if isinstance(paths, str):
                paths = [paths]
            placeholders = ",".join(["%s"] * len(paths))
            conditions.append(f"path IN ({placeholders})")
            params.extend(paths)

        # 角色稀有度过滤（支持多选）
        if rarities := data_dt.get("rarities"):
            if isinstance(rarities, str):
                rarities = [rarities]
            placeholders = ",".join(["%s"] * len(rarities))
            conditions.append(f"rarity IN ({placeholders})")
            params.extend(map(str, rarities))  # 统一转为字符串

        # 构建完整SQL
        sql = """
            SELECT
                id,
                NAME,
                element,
                path,
                rarity,
                position
            FROM
                characters
            """
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        try:
            # 执行查询（自动处理连接）
            result = MySQLExecutor.execute(
                sql=sql,
                params=tuple(params),  # 必须转为元组
                fetch_all=True
            )
            keys = [
                "id", "name", "element",
                "path", "rarity", "position"
            ]
            # 结果整合为list
            characters_lt = [tools.tuple_to_dict(keys=keys, data=row) for row in result]
            if not characters_lt:
                return None
            for row in characters_lt:
                row['character_image_1'] = f"""/static/images/characters/{row.get('id')}/{row.get('name')}_1.png"""
                row['character_image_2'] = f"""/static/images/characters/{row.get('id')}/{row.get('name')}_2.png"""
                row['character_image_3'] = f"""/static/images/characters/{row.get('id')}/{row.get('name')}_3.png"""
            return characters_lt
        except Exception as e:
            print(f"数据库查询异常: {str(e)}")
            return None

    @classmethod
    def get_character_talent(cls, char_id):
        """
        查询单个角色的天赋和技能信息
        :return:
        """
        try:
            query_sql = """
                    SELECT
                        skill_name,
                        skill_type,
                        skill_description
                    FROM
                        character_talent
                    WHERE
                        character_id = %s
                """
            result = MySQLExecutor.execute(
                query_sql,
                params=(char_id,),
                fetch_all=True
            )
            if not result:  # 处理空结果
                return None
            return result
        except Exception as e:
            logger.error(f"角色技能信息查询出错: {str(e)}")
            return None

    @classmethod
    def get_character_constellation(cls, char_id):
        """
        查询单个角色的星魂信息
        :return:
        """
        try:
            query_sql = """
               SELECT
                   character_id,
                   constellation_name,
                   constellation_level,
                   constellation_description
               FROM
                   character_constellation
               WHERE
                   character_id = %s
               """
            result = MySQLExecutor.execute(
                query_sql,
                params=(char_id,),
                fetch_all=True
            )
            if not result:  # 处理空结果
                return None
            return result
        except Exception as e:
            logger.error(f"角色星魂信息查询出错: {str(e)}")
            return None

    @classmethod
    def get_light_cone(cls, char_id):
        """
        获取角色适配光锥
        :param char_id:
        :return:
        """
        try:
            query_sql = """
               SELECT
                    * 
               FROM
                   light_cone
                   RIGHT JOIN character_light_cones ON light_cone.name = character_light_cones.light_cone_name
               WHERE
                   character_id = %s
               """
            result = MySQLExecutor.execute(
                query_sql,
                params=(char_id,),
                fetch_all=True
            )
            if not result:  # 处理空结果
                return None
            return result
        except Exception as e:
            logger.error(f"适配光锥信息查询出错: {str(e)}")
            return None
