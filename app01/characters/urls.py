
from django.urls import path
from app01.characters import char_views

app_name = "characters"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/<str:character_id>/
    path('<str:character_id>/', char_views.find_character),  # 查询游戏角色信息
]
