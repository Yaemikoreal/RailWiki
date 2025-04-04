# MySQL配置
MYSQL_DATABASES = {
    'NAME': 'rail',        # 数据库名
    'USER': 'Yaemiko',     # 用户名
    'PASSWORD': '200212',  # 密码
    'HOST': 'localhost',   # 数据库地址
    'PORT': '3306',        # 端口
    'CONN_MAX_AGE': 300,   # 连接池保持时间（秒）
}

# MongoDB配置
MONGO_DATABASES = {
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': 27017,
    'MONGO_USER': 'Yaemiko',
    'MONGO_PASS': '200212',
    'MONGO_AUTH_DB': 'school',
    'MONGO_DB_NAME': 'school'
}
