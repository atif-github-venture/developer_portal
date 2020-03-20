from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('group/', views.group, name='group'),
    path('access/', views.access, name='access'),
    path('home/', views.home, name='home'),
]
