# 工具类计算函数

def list_to_quoted_string(input_list, separator=", "):
    """
    将列表转换为带单引号并用指定分隔符连接的字符串。

    :param input_list: 输入的列表（元素可以是任何类型）
    :param separator: 分隔符，默认为 ", "
    :return: 转换后的字符串
    """
    if not isinstance(input_list, list):
        raise ValueError("输入必须是一个列表")

    # 将每个元素转为字符串并添加单引号
    quoted_items = [f"'{str(item)}'" for item in input_list]

    # 使用指定分隔符拼接
    return separator.join(quoted_items)


def tuple_to_dict(keys, data):
    """
    将元组数据按照固定的 key 列表转换为字典。

    :param keys: 固定的 key 列表（字段名列表）
    :param data: 元组数据
    :return: 转换后的字典
    """
    if not isinstance(keys, list):
        raise ValueError("keys 必须是一个列表")
    if not isinstance(data, (tuple, list)):
        raise ValueError("data 必须是一个元组或列表")
    if len(keys) != len(data):
        raise ValueError("keys 的长度必须与 data 的长度一致")

    # 使用 zip 将 keys 和 data 组合成字典
    return dict(zip(keys, data))


def calculate_talents(result: tuple) -> []:
    talent_data = []
    for it in result:
        data_dt = {
            "name": it[0],
            "type": it[1],
            "description": it[2]
        }
        talent_data.append(data_dt)
    return talent_data


def calculate_constellation(result: tuple) -> []:
    constellation = []
    for it in result:
        data_dt = {
            "name": it[1],
            "level": it[2],
            "description": it[3],
            "image": f"""/static/images/characters/{it[0]}/constellation_{it[2]}.png"""
        }
        constellation.append(data_dt)
    return constellation


def calculate_light_cone(result: tuple) -> []:
    light_cone = []
    for it in result:
        data_dt = {
            "name": it[1],
            "rarity": it[2],
            "base_attack": it[3],
            "base_hp": it[4],
            "base_defense": it[5],
            "skill_name": it[6],
            "skill_effect": it[7],
            "cone_image": f"""/static/images/lightcone/{it[1]}.png"""
        }
        light_cone.append(data_dt)
    return light_cone
