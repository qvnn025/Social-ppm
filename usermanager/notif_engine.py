from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(to_user=request.user,is_read=False).count()
    else:
        count = 0
    return {'unread_notifs': count}