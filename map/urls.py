from django.urls import path, include
from . import views
urlpatterns = [
    # path('', views.map, name='map'),
    # path('', views.ViewWells, name='ViewWells'),
    path('', views.heir_map, name='heir_map'),
    

]
