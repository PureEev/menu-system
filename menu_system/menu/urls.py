from django.urls import path
from .views import home

app_name = 'menu'

urlpatterns = [
    path('', home, name='home'),
]