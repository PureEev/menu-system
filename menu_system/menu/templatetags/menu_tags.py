from django import template
from ..models import MenuItem
from collections import defaultdict

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path.strip('/').split('/')
    menu_name_url = menu_name.replace(' ', '_')

    items = (
        MenuItem.objects
        .filter(menu__name=menu_name)
        .select_related('parent')
        .order_by('order')
    )
    if not items.exists():
        return {
            'main_menu': {'title': menu_name, 'url': f'/{menu_name_url}/'},
            'menu_items': [],
            'active_item': None,
            'show_children': False,
            'request': request,
        }

    by_parent = defaultdict(list)
    for it in items:
        by_parent[it.parent_id].append(it)

    active_item = None
    parent_id = None
    subpath = current_path[1:] if current_path and current_path[0] == menu_name_url else []
    for part in subpath:
        title = part.replace('_', ' ')
        for it in by_parent[parent_id]:
            if it.title == title:
                active_item = it
                parent_id = it.id
                break
        else:
            break

    active_ancestors = []
    if active_item:
        cur = active_item
        while cur:
            active_ancestors.insert(0, cur)
            cur = cur.parent

    show_children = active_item is not None

    def build(nodes):
        tree = []
        for node in nodes:
            if show_children and (node in active_ancestors):
                node.children = build(by_parent.get(node.id, []))
            else:
                node.children = []
            path_parts = []
            cur = node
            while cur:
                path_parts.insert(0, cur.title.replace(' ', '_'))
                cur = cur.parent
            node.url = '/' + menu_name_url + '/' + '/'.join(path_parts) + '/'
            tree.append(node)
        return tree

    menu_tree = build(by_parent.get(None, []))

    return {
        'main_menu': {'title': menu_name, 'url': f'/{menu_name_url}/'},
        'menu_items': menu_tree,
        'active_item': active_item,
        'show_children': show_children,
        'request': request,
    }
