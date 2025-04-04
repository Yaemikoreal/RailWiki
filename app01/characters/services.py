from db.executor_utils import MySQLExecutor


class CharacterService:
    @classmethod
    def get_character(cls, character_id):
        """
        获取单个角色信息并返回角色信息字典
        :param character_id: 角色ID
        :return:
        """
        try:
            result = MySQLExecutor.execute(
                "SELECT * FROM characters WHERE id = %s",
                params=(character_id,),
                fetch_one=True
            )
            if not result:  # 处理空结果
                return None
            keys = [
                "character_id", "character_name", "character_element",
                "character_path", "character_rarity", "character_position",
                "character_description", "character_release_date"
            ]
            character_dt = dict(zip(keys, result))
            return character_dt
        except Exception as e:
            print(str(e))
