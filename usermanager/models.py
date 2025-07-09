import os
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

#CLOUDINARY
ENVIRONMENT=os.environ.get("ENVIRONMENT") in ['production', True]

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )
    bio=models.TextField(blank=True)
    # cloudinary switch
    if ENVIRONMENT:
        from cloudinary.models import CloudinaryField
        pfp = CloudinaryField('pf_image', blank=True, null=True)
    else:
        pfp = models.ImageField(upload_to='pfps/',blank=True,null=True)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    class Meta:
        permissions = [
            ("can_ban_user", "Can ban other users"),
        ]

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model  = User
        fields = ('username','email','password1','password2')


class Notification(models.Model):
    NOTIF_TYPES = [
        ('friend_request',  'Friend Request'),
        ('friend_accept',   'Friend Request Accepted'),
        ('post_like',       'Post Like'),
        ('comment_like',    'Comment Like'),
        ('post_comment',    'Post Comment'),
        ('post_share',      'Post Share'),
    ]

    to_user     = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='notifications',
                                    on_delete=models.CASCADE)
    from_user   = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='+',
                                    on_delete=models.CASCADE)
    notif_type  = models.CharField(max_length=20, choices=NOTIF_TYPES)
    created     = models.DateTimeField(auto_now_add=True)
    is_read     = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType,null = True,blank = True,on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField(null = True,blank = True)
    target       = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created']


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sent_requests',on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='received_requests',on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        self.status = 'accepted'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

class Friendlist(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='friendlists_sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='friendlists_received')
    created= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('from_user', 'to_user')]

