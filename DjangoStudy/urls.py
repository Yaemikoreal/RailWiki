"""
URL configuration for DjangoStudy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin

from app01.views import index,home

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 后台
    path('', home, name='home(wiki index)'),
    path('wikiindex/', index, name='wiki index'),
    # API 路由分配
    path('api/characters/', include('app01.characters.urls')),  # 角色相关路由
    path('api/guides/', include('app01.guides.urls')),  # 攻略相关路由

]

