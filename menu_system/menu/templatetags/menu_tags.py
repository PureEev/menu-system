from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from ..models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    current_path = request.path if request else ''

    # Единый запрос к БД с фильтрацией по имени меню
    qs = MenuItem.objects.filter(menu__name=menu_name).select_related('parent').order_by('order')
    items = list(qs)

    if not items:  # Если меню пустое, возвращаем пустую строку
        return ''

    id_map = {}
    for item in items:
        # Резолвим URL с учётом menu_name в fallback
        if item.is_named_url and item.url:
            try:
                item.resolved_url = reverse(item.url)
            except NoReverseMatch:
                item.resolved_url = '#'
        elif item.url:
            # Если URL явно указан, используем как есть
            item.resolved_url = item.url
            # menu/templatetags/menu_tags.py
        else:
            # Формируем URL с использованием namespace и корректных параметров
            try:
                item.resolved_url = reverse(
                    'menu:menu_item_detail',  # Добавляем namespace
                    kwargs={
                        'menu_name': menu_name,
                        'slug': item.slug
                    }
                )
            except NoReverseMatch:
                item.resolved_url = '#'

        item.children_list = []
        item.is_active = (item.resolved_url == current_path)
        item.is_open = False
        id_map[item.id] = item

    # Построение дерева
    roots = []
    for item in items:
        if item.parent_id:
            parent = id_map.get(item.parent_id)
            if parent:
                parent.children_list.append(item)
        else:
            roots.append(item)

    # Определение активных элементов и раскрытие родителей
    active_item = next((item for item in items if item.is_active), None)
    if active_item:
        p = active_item.parent
        while p:
            p.is_open = True
            p = p.parent
        active_item.is_open = True

    # Рендер HTML
    def render_list(nodes):
        if not nodes:
            return ''
        html = ['<ul class="menu-list">']
        for node in nodes:
            classes = []
            if node.is_active:
                classes.append('active')
            if node.is_open or node == active_item:
                classes.append('open')
            class_attr = f' class="{" ".join(classes)}"' if classes else ''
            html.append(f'<li{class_attr}>')
            html.append(f'<a href="{node.resolved_url}">{node.name}</a>')
            if node.children_list and (node.is_open or node == active_item):
                html.append(render_list(node.children_list))
            html.append('</li>')
        html.append('</ul>')
        return ''.join(html)

    # Сборка контейнера
    container = [
        f'<div class="menu-container" id="menu-{menu_name}">',
        f'<div class="menu-title">{menu_name}</div>',
        render_list(roots),
        '</div>'
    ]

    print(f"Menu: {menu_name}, Items: {[(item.name, item.resolved_url) for item in items]}")
    return mark_safe(''.join(container))