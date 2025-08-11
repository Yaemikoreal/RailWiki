import json
import re

import requests
from bs4 import BeautifulSoup

from db.db_utils import MySQLManager
from db.executor_utils import MySQLExecutor

class CharactersMsgGet:
    def __init__(self):
        self.data_lt = []
        self.any_char_url = "https://act-api-takumi-static.mihoyo.com/common/blackboard/sr_wiki/v1/content/info?app_sn=sr_wiki&content_id="
        self.char_id_lt = self.read_all_character_msg()

    def read_html(self):
        with open('data.json', 'r', encoding='utf-8') as f:
            html = f.read()
        data_dt = json.loads(html)
        char_lt = data_dt['data']['list'][0].get('list')
        return char_lt

    def get_any_character_msg(self, char):
        char_id = char.get('content_id')
        data_dt = {
            'char_id': char_id,
            'char_name': char.get('title'),
            'char_icon': char.get('icon'),
            'char_url': f"https://bbs.mihoyo.com/sr/wiki/content/{char_id}/detail?bbs_presentation_style=no_header"
        }
        self.data_lt.append(data_dt)

    def get_char_ext(self, char_ext_lt, char_dt):
        for item in char_ext_lt:
            key, value = item.split("/", 1)  # 只分割第一个/，提高分割效率
            if key == "属性":
                char_dt['element'] = value
            elif key == "命途":
                char_dt['path'] = value
            elif key == "星级":
                char_dt['rarity'] = value
        return char_dt

    def get_char_story(self, any_char_dt, char_dt):
        msg_dt = any_char_dt['data']['content']
        har_story_dt = msg_dt.get('rpg_new_tmp_content')
        if har_story_dt:
            char_story_dt = har_story_dt['modules'][8]['components'][0]['data']
            char_story_dt = json.loads(char_story_dt)
            char_dt["description"] = char_story_dt['detail']
            return char_dt
        else:
            char_story_text = msg_dt['contents'][2]['text']
            char_soup = BeautifulSoup(char_story_text, 'html.parser')
            char_story_tag = char_soup.find('div', class_='obc-tmpl__rich-text')
            char_story_text = char_story_tag.find('p', style=True).get_text()
            char_dt["description"] = char_story_text
            return char_dt

    def get_char_basis_msg(self, any_char_dt):
        """
        整合角色基础信息，该信息输入到characters表
        :return:
        """
        # 该角色的信息字典,角色id以及角色名称
        char_dt = {"id": any_char_dt['data']['content']['id'], "name": any_char_dt['data']['content']['title']}

        char_dt = self.get_char_story(any_char_dt, char_dt)
        # 角色属性，角色星级，角色命途
        char_ext = any_char_dt['data']['content']['ext']
        char_ext = json.loads(char_ext)
        char_ext_lt = json.loads(char_ext['c_18']['filter']['text'])

        char_dt = self.get_char_ext(char_ext_lt, char_dt)
        return char_dt

    def get_all_character_msg(self, char_id):
        """
        获取单个角色详细信息
        :return:
        """
        any_char_url = self.any_char_url + str(char_id)
        req = requests.get(any_char_url)
        any_char_dt = json.loads(req.text)
        # 整合角色基础信息
        char_dt = self.get_char_basis_msg(any_char_dt)
        print(f"{char_dt} 获取完毕!!")
        print("===" * 20)
        return char_dt

    def clear_existing_data(self, all_char_lt):
        """
        清除已有数据内容
        :return:
        """
        new_char_lt = []
        for char in all_char_lt:
            char_id = char['id']
            if char_id not in self.char_id_lt:
                new_char_lt.append(char)
                print(f"角色【{char.get('name')}】加入！！！")
            else:
                print(f"角色【{char.get('name')}】已存在！！！")
        return new_char_lt

    def read_all_character_msg(self):
        """
        读取数据库已有所有角色的id
        :return:
        """
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
        result = MySQLExecutor.execute(sql, fetch_all=True)
        char_id_lt = [t[0] for t in result]
        return char_id_lt

    def data_into(self, new_char_lt):
        """
        数据写入
        :return:
        """
        # 转换rarity值为数字
        rarity_map = {'一星': 1, '二星': 2, '三星': 3, '四星': 4, '五星': 5}

        for item in new_char_lt:
            if 'rarity' in item and isinstance(item['rarity'], str):
                item['rarity'] = rarity_map.get(item['rarity'], 0)  # 默认0如果不在映射中
        with MySQLManager.get_conn() as conn:
            with conn.cursor() as cursor:
                try:
                    # 使用 %(name)s 格式的命名参数
                    sql = """
                       INSERT INTO characters 
                       (id, name, element, path, rarity, description) 
                       VALUES (
                           %(id)s, 
                           %(name)s, 
                           %(element)s, 
                           %(path)s, 
                           %(rarity)s, 
                           %(description)s 
                       )
                           """
                    cursor.executemany(sql, new_char_lt)
                    conn.commit()
                    print(f"成功写入 {len(new_char_lt)} 条数据！")
                except Exception as e:
                    conn.rollback()
                    print(f"数据写入失败: {e}")
                    raise  # 可以选择重新抛出异常或处理

    def calculate(self):

        # 读取html进行解析
        char_list = self.read_html()
        for char in char_list:
            # 解析出角色信息
            self.get_any_character_msg(char)
        all_char_lt = []
        for item in self.data_lt:
            char_id = item['char_id']
            char_dt = self.get_all_character_msg(char_id)
            all_char_lt.append(char_dt)
        # 清除已有数据内容
        new_char_lt = self.clear_existing_data(all_char_lt)
        self.data_into(new_char_lt)



def test():
    c = CharactersMsgGet()
    c.calculate()


if __name__ == '__main__':
    test()
