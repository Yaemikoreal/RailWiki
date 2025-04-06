# 角色Wiki子路由
from django.urls import path
from .CharViews import find_characters_list, character_detail, show_character_detail

app_name = "characters"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/<int:pk>/
    path('paginationquery/', find_characters_list),  # 角色列表分页查询
    path('<int:pk>/', character_detail),  # 查询单个游戏角色信息
    # 整合渲染+数据的路由
    path('character_detail/', show_character_detail, name='character-detail'),
]
