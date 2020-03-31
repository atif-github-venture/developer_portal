from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('admin/', views.admin, name='admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('swaggerview/', views.swaggerview, name='swaggerview'),
    path('swaggeredit/', views.swaggeredit, name='swaggeredit'),
    path('dependency/', views.dependency, name='dependency'),
]
