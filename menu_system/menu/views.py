# views.py
from django.shortcuts import render, get_object_or_404
from .models import MenuItem

def home(request):
    """
    Главная страница на '/' с отрисовкой двух основных меню.
    В шаблоне menu/home.html будут вызываться:
      {% draw_menu 'Main_menu_1' %}
      {% draw_menu 'Main_menu_2' %}
    Блоку {% if item %}…{% endif %} он не мешает, потому что item не передаётся.
    """
    return render(request, 'menu/home.html')


def menu_item_detail(request, menu_name, slug):
    item = get_object_or_404(MenuItem, menu__name=menu_name, slug=slug)
    return render(request, 'menu/home.html', {'item': item})
