from django.shortcuts import render

def home(request):
    return render(request, 'menu/home/home.html')