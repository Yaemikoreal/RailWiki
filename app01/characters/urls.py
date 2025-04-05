
from django.urls import path
from .CharViews import find_characters_list, find_character

app_name = "characters"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/<str:character_id>/
    path('paginationquery/', find_characters_list),  # 角色列表分页查询
    path('any/', find_character),  # 查询游戏角色信息
]
