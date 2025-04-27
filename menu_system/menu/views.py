from django.shortcuts import render


def home(request):
    return render(request, 'menu/home.html')

def menu_root(request, menu_name):
    return render(request, 'menu/home.html', {'menu_name': menu_name})

def menu_item_detail(request, menu_name, subpath):
    return render(request, 'menu/home.html', {'menu_name': menu_name})