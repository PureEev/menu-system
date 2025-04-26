# menu/urls.py
from django.urls import path
from .views import home, menu_item_detail

app_name = 'menu'

urlpatterns = [
    path('', home, name='home'),
    # Один универсальный путь с параметрами
    path('<str:menu_name>/<slug:slug>/', menu_item_detail, name='menu_item_detail'),
]