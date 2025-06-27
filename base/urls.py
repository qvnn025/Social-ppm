from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-post/', views.createpost, name='create-post'),
    path('update-post/<str:pk>/', views.updatepost, name='update-post'),
    path('delete-post/<str:pk>/', views.deletepost, name='delete-post'),
]