from db.db_utils import MongoManager


class Strategy:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def save(self):
        db = MongoManager.get_db()
        return db.strategies.insert_one({
            'title': self.title,
            'content': self.content
        })