from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('group/', views.group, name='group'),
    path('access/', views.access, name='access'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('swaggerview/', views.swaggerview, name='swaggerview'),
    path('swaggeredit/', views.swaggeredit, name='swaggeredit'),
    path('dependency/', views.dependency, name='dependency'),
]
