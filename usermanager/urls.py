from django.urls import path
from . import views

app_name = 'usermanager'

urlpatterns = [
    path('login/', views.loginview, name='user-login'),
    path('register/', views.registeruser, name='user-register'),
    path('logout/', views.logoutview, name='user-logout'),
    path('profile/<int:pk>/', views.profilerender, name='user-profile'),
    path('email-prompt/', views.emailprompt, name='email-prompt'),
    path('send-request/<int:pk>/', views.sendreq, name='send-req'),
    path('respond-request/<int:notif_id>/<str:action>/', views.respondreq, name='respond-req'),
    path('notif-inbox/', views.notifbox, name='inbox'),
    path('user/<int:user_id>/ban/', views.ban, name='ban'),
]