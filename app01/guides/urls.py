# characters/urls.py
from django.urls import path
from .GuidesViews import conventional_damage_calculation, get_light_cones

app_name = "guides"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/
    # path('api/characters/<str:character_id>/', views.CharacterService.get_character),  #

    path('light_cones/', get_light_cones),  # 攻略查询
    # GET /api/guides/
]