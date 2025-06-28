from django.db import models
from django.conf import settings

#POST TOPIC (tags)
class Topic(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#POST THREAD
class Room(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.SET_NULL,null = True, related_name="posts")
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    #date = models.DateTimeField(auto_now_add=True)
    description =models.TextField(null=True, blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name
#THREAD COMMENTS
class Message(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]