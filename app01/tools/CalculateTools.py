# 工具类计算函数
import os
import django
import requests
from urllib.parse  import urlparse
# 配置 Django 环境（必须在所有 Django 导入和模型操作前调用）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoStudy.settings')
django.setup()

from django.conf import settings


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
            'id': it[0],
            "name": it[1],
            "type": it[2],
            'tag':  it[3],
            "description": it[4]
        }
        data_dt["skill_img"] = f"/static/images/characters/{data_dt['id']}/img_{data_dt['type']}_{data_dt['tag']}.png"
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
            "base_attack": it[2],
            "base_hp": it[3],
            "base_defense": it[4],
            "skill_name": it[5],
            "skill_effect": it[6],
            "cone_image": f"""/static/images/lightcone/{it[1]}.png"""
        }
        light_cone.append(data_dt)
    return light_cone


def calculate_character(character_data: dict) -> dict:
    character_data[
        'character_image_1'] = f"""/static/images/characters/{character_data.get('id')}/{character_data.get('name')}_1.png"""
    character_data[
        'character_image_2'] = f"""/static/images/characters/{character_data.get('id')}/{character_data.get('name')}_2.png"""
    character_data[
        'character_image_anther'] = f"""/static/images/characters/{character_data.get('id')}/{character_data.get('name')}_anther.png"""
    character_data['element_img'] = f"""/static/images/general/attribute/{character_data.get('element')}.png"""
    character_data['path_img'] = f"""/static/images/general/paths/{character_data.get('path')}.png"""
    return character_data


def download_image(url, save_dir=None, filename=None, overwrite=False, iswhere='characters'):
    """
    从URL下载图片并保存到 Django 项目的静态目录

    参数:
        url (str): 图片URL
        save_dir (str): 可选的子目录（相对于 static/images/characters/）
        filename (str): 自定义文件名（默认从URL提取）
        overwrite (bool): 如果文件存在是否覆盖（默认False）
        iswhere (str): 填入存入地址，默认为角色文件夹

    返回:
        dict/None: 包含保存路径信息的字典，如果文件已存在或下载失败则返回None
    """
    try:
        # 1. 构建目标路径
        base_dir = os.path.join(
            settings.BASE_DIR,
            'app01',
            'static',
            'images',
            iswhere
        )

        # if save_dir is not None:
        # 处理子目录
        target_dir = os.path.join(base_dir, save_dir) if save_dir else base_dir
        os.makedirs(target_dir, exist_ok=True)

        # 2. 确定文件名
        if not filename:
            # 从URL提取更安全的文件名
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path) or "unnamed_image.jpg"

            # 确保有正确的文件扩展名
            if not os.path.splitext(filename)[1]:
                try:
                    # 发送HEAD请求获取内容类型
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.head(url, headers=headers, timeout=5)
                    response.raise_for_status()

                    content_type = response.headers.get('content-type', '')
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        filename += '.jpg'
                    elif 'png' in content_type:
                        filename += '.png'
                    elif 'webp' in content_type:
                        filename += '.webp'
                    else:
                        filename += '.jpg'  # 默认后缀
                except:
                    filename += '.jpg'  # 如果HEAD请求失败，使用默认

        # 3. 检查文件是否已存在
        save_path = os.path.join(target_dir, filename)
        if os.path.exists(save_path) and not overwrite:
            print(f"文件已存在，跳过下载: {save_path}")
            return None

            # 4. 下载文件
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()

        # 5. 保存文件（使用临时文件确保原子性写入）
        temp_path = f"{save_path}.temp"
        try:
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(1024 * 8):  # 8KB chunks
                    if chunk:
                        f.write(chunk)

                        # 重命名为正式文件
            os.replace(temp_path, save_path)
        except:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

        # 6. 返回路径信息
        rel_path = os.path.relpath(
            save_path,
            start=os.path.join(settings.BASE_DIR, 'app01', 'static')
        ).replace('\\', '/')

        print(f"图片下载成功: {save_path}")
        return {
            'abs_path': save_path,
            'rel_path': rel_path,
            'filename': os.path.basename(save_path)
        }

    except requests.exceptions.RequestException as e:
        print(f"下载请求失败: {str(e)}")
        return None
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        return None


if __name__ == '__main__':
    url = 'https://act-upload.mihoyo.com/sr-wiki/2025/08/06/331632599/5a63eb614e744c7fa0451ec565b55356_1575260239918394995.png'
    save_dir = '5582'
    filename = 'constellation_1.png'
    download_image(url, save_dir, filename)
