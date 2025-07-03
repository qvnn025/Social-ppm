from django.urls import path
from . import views

app_name = 'usermanager'

urlpatterns = [
    path('login/', views.loginview, name='user-login'),
    path('register/', views.registeruser, name='user-register'),
    path('logout/', views.logoutview, name='user-logout'),
    path('profile/<int:pk>/', views.profilerender, name='user-profile'),
]