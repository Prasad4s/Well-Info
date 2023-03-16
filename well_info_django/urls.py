from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('registration/', include('django.contrib.auth.urls')),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('', include('map.urls')),
    path('', include('forms.urls')),
    # path('', include('pwa.urls')),
]
