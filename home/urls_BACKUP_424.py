from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    # path('', views.viewWells, name='viewWells'),
    path('',views.view_wells, name='view_wells'),
    path('viewWells/',views.viewWells, name='viewWells'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_request, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/', views.register_request, name='register'),
    path('captwellpic/', views.captwellpic, name='captwellpic'),
    path('uploadwellpic/', views.uploadwellpic, name='uploadwellpic'),
    
    path('well_info/', views.well_info, name='well_info'),
    path('graph_well/', views.graph_well, name='graph_well'),
    path('view_entered_details/', views.view_entered_details, name="view_entered_details"),
    # path('delete/<int:id>', views.delete, name='delete')
    path('edit_well_picture/<int:pk>/', views.edit_well_picture, name='edit_well_picture'),
<<<<<<< HEAD
    path('tutorial/',views.tutorial, name='tutorial'),
    path('resources/',views.resources, name='resources'),
    #  path('view_wells/',views.view_wells, name='view_wells'),
=======
# For registration form
    path('loginForm/',views.loginForm, name='loginForm'),
    path('registerForm/',views.registerForm, name='registerForm'),
    path('form/',views.form, name='form'),
    path('add_tasks/',views.add_tasks, name='add_tasks'),
    path('home/',views.home, name='home'),
    
>>>>>>> d9cb9ee5d209c2eac6582573ab6963145223e315
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
