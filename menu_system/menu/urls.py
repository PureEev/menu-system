from django.urls import path
from .views import home, menu_item_detail, menu_root

app_name = 'menu'

urlpatterns = [
    path('', home, name='menu_home'),
    path('<str:menu_name>/', menu_root, name='menu_root'),
    path('<str:menu_name>/<path:subpath>/', menu_item_detail, name='menu_item'),
]