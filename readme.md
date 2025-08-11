# RailWiki
**RailWiki** - 星穹铁道的Wiki
 
## 目录
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [安装指南](#-安装指南)
  - [开发环境](#开发环境配置)
  - [生产环境](#生产环境部署)
- [项目结构](#-项目结构)
 
## 🌟 功能特性 
- ✅ **核心功能1** - 功能描述 
- 🎨 **核心功能2** - 功能描述 
- 🔒 **安全特性** - 功能描述
- ⚡ **性能优化** - 功能描述 
 
## 🛠️ 技术栈
| 类别       | 技术选型                 |
|------------|--------------------------|
| 前端       | HTML5, CSS3, JavaScript  |
| 后端       | Django 5.2/Python 3.11 |
| 数据库     | MySQL/MongoDB           |
| 基础设施   | ~~Docker, Nginx, Redis~~     |
 
## 📦 安装指南 
 
### 开发环境配置 
```bash
# 1. 克隆仓库 
git clone https://github.com/Yaemikoreal/RailWiki.git
 
# 2. 设置虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
 
# 3. 安装依赖
pip install -r requirements.txt 

# 4. 启动服务 
python manage.py  runserver 
```
📂 项目结构

```bash
📁 starrail_project/
├── 📁 DjangoStudy/             # 全局配置
│    ├── 📄 settings.py         # Django主配置
│    ├── 📄 urls.py             # 主路由
│    ├── 📄 logger_config.py    # 日志打印设置
│    ├── 📄 wsgi.py             
│    └── 📄 asgi.py
│
│
├── 📁 db/                      # 数据库管理
│    ├── 📄 db_settings.py      # 数据库连接配置（独立文件）
│    ├── 📄 db_utils.py         # 连接池管理
│    └── 📄 executor_utils.py   # 数据库SQL执行器管理
│    
│
├── 📁 app01/                    # 应用模块
│    ├── 📁 characters/         # 角色/装备模块（MySQL）
│    │    ├── 📄 MongoModels.py # 角色模型类
│    │    ├── 📄 Services.py    # 角色相关数据库查询操作
│    │    ├── 📄 urls.py        # 子路由
│    │    └── 📄 CharViews.py   # 角色相关视图函数
│    │
│    ├── 📁 strategies/         # 攻略模块（MongoDB）
│    │    
│    ├── 📁 static/             # 静态资源
│    │    └── 📁 images/        # 图片资源
│    │
│    ├── 📁 templates/          # 前端模板
│    │    ├── 📄 character_detail.html # 角色详情页
│    │    └── 📄 wiki_index.html    # 网页主体页
│    │
│    │
│    └── 📁 tools/              # 工具
│        └── 📄 CalculateTools.py # 工具类计算函数
│
├── 📁 DataGet/                 # 数据获取 
│      └── 📄 characters_msg_get.py # 获取角色基础信息
│ 
│ 
├── 📄 requirements.txt    
│     
└── 📄 manage.py                # Django管理脚本
```
