from django.urls import path, include
from . import views
urlpatterns = [
    path('basicinfo', views.basicinfo, name='basicinfo'),
]
