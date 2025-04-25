from django import template
from django.urls import resolve, reverse, NoReverseMatch, Resolver404
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info
    try:
        active_url = resolve(current_url).url_name
    except Resolver404:
        active_url = None

    # Fetch all menu items in one query
    all_items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    # Build tree structure
    items_by_id = {item.id: item for item in all_items}
    root_items = [item for item in all_items if item.parent_id is None]

    for item in all_items:
        if item.parent_id:
            parent = items_by_id[item.parent_id]
            if not hasattr(parent, 'children'):
                parent.children = []
            parent.children.append(item)

    # Determine active item
    active_item = None
    for item in all_items:
        if item.is_named_url:
            try:
                item.actual_url = reverse(item.url)
            except NoReverseMatch:
                item.actual_url = item.url
        else:
            item.actual_url = item.url

        if (item.is_named_url and item.url == active_url) or item.actual_url == current_url:
            active_item = item
            break

    # Determine expanded items (ancestors and active item)
    expanded_items = set()
    if active_item:
        current = active_item
        while current:
            expanded_items.add(current.id)
            current = current.parent

    return {
        'root_items': root_items,
        'expanded_items': expanded_items,
        'active_item': active_item,
    }