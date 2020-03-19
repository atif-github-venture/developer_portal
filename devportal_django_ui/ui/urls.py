from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.home),
#     path('about/', views.about),
# ]

urlpatterns = [
    path('', views.base, name='base'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path(r'^userlogin/$', views.user_login, name='user_login'),
]
