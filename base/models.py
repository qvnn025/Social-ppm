from django.db import models
from django.conf import settings
from django.urls import reverse

#POST TOPIC (tags)
class Topic(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TopicCount(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

#POST THREAD
class Room(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.SET_NULL,null = True, related_name="posts")
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description =models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='room_images/', blank=True,null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_rooms',blank=True)
    #link for notif
    def get_absolute_url(self):
        return reverse('base:room', args=[self.pk])


    class Meta:
        ordering = ['-updated', '-created']
        #MOD PERMS
        permissions = [
            ("can_delete_any_room", "Can delete any room")
        ]
    def __str__(self):
        return self.name
#THREAD COMMENTS
class Message(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    deleted_by_moderator = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked_comments', blank=True)
    def get_absolute_url(self):
        url = reverse('base:room', args=[self.room.pk])
        return f"{url}#comment-{self.pk}"
    #MOD PERMS
    class Meta:
        permissions = [
            ("can_delete_any_message", "Can delete any message")
        ]

    def __str__(self):
        if self.deleted_by_moderator:
            return "[deleted]"
        return self.body[0:50]

#post share
class Share(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original= models.ForeignKey(Room, on_delete=models.CASCADE, related_name='shares')
    caption= models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    image= models.ImageField(upload_to='shares/', blank=True, null=True)
    created= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']