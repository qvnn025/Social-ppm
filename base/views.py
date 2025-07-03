from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Message, TopicCount
from .forms import PostForm
from django.db.models import Count, Q
from django.utils import timezone


def home(request):
    since = timezone.now() - timedelta(hours=24)
    rooms = (
        Room.objects
        .annotate(
            recent_comments=Count(
                'message',
                filter=Q(message__created__gte=since)
            )
        )
        .order_by('-recent_comments', '-updated')
    )
    return render(request, 'base/home.html', {'rooms': rooms})

def room(request, pk):
   room = get_object_or_404(Room, pk=pk)
   #TOPIC PREFERENCE COUNT
   affinity, _ = TopicCount.objects.get_or_create(
       user=request.user, topic=room.topic
   )
   affinity.score += 1
   affinity.save()
   comments = room.message_set.all().order_by('-created')
   if request.method == 'POST':
       message = Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
       return redirect('base:room',pk=room.id)
   context = {'room':room, 'comments':comments}
   return render(request, 'base/room.html', context)

@login_required(login_url='usermanager:user-login')
def createpost(request):
    form = PostForm()

    if request.method == 'POST':
       form = PostForm(request.POST)
       if form.is_valid():
              form.save()
              return redirect('base:home')

    context={"form":form}
    return render(request, "base/room-form.html", context)

@login_required(login_url='usermanager:user-login')
def updatepost(request, pk):
    room = Room.objects.get(id=pk)
    form = PostForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You can't do that")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    context={'form':form}
    return render(request, 'base/room-form.html', context)

@login_required(login_url='usermanager:user-login')
def deletepost(request, pk):
    room = Room.objects.get(id=pk)
    if request.user == room.host or request.user.has_perm('base.delete_room'):
     if request.method == 'POST':
       room.delete()
       return redirect('base:home')

    return render(request, 'base/delete.html', {"obj":room})

@login_required(login_url='usermanager:user-login')
def deletecomment(request, pk):
    comment = get_object_or_404(Message, pk=pk)
    if request.user == comment.user or request.user.has_perm('base.delete_message'):
     if request.method == 'POST':
       comment.deleted_by_moderator = True
       comment.save()
       room = comment.room
       return redirect('base:room',pk=room.id)

    return render(request, 'base/delete.html', {"obj":comment})

def foryoufeed(request):
    top_topics = (
        TopicCount.objects
        .filter(user=request.user)
        .order_by("-score")
        .values_list("topic", flat=True)[:3]
    )
    rooms = (
        Room.objects
        .filter(topic__in=top_topics)
        .order_by("-updated")[:50]
    )
    return render(request, "base/for_you.html", {"rooms": rooms})


