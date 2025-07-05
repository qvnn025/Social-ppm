from django.contrib import admin
from .models import Profile, FriendRequest, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pfp')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'from_user', 'notif_type', 'is_read', 'created')

