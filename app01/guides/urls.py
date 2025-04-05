# characters/urls.py
from django.urls import path
from . import GuidesViews

app_name = "characters"  # 命名空间（可选）

urlpatterns = [
    # GET /api/characters/
    # path('api/characters/<str:character_id>/', views.CharacterService.get_character),  #

]