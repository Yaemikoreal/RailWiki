# app/views.py
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'wiki_index.html')


def home(request):
    # 重定向到 wiki index 页面
    return redirect('wiki index')  # 使用命名 URL
