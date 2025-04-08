# 角色Wiki子路由
from django.urls import path
from .CharViews import find_characters_list, character_detail, show_character_detail, find_character_talent

app_name = "characters"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/<int:pk>/
    path('paginationquery/', find_characters_list),  # 角色列表分页查询
    path('<int:pk>/', character_detail),  # 单个游戏角色信息查询
    # 整合渲染+数据的路由
    path('character_detail/', show_character_detail, name='character-detail'),  # 角色详情页
    path('talent/<int:char_id>/', find_character_talent, name='character_talent'),  # 角色天赋技能信息查询
]
