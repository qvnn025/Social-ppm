from datetime import timedelta
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from usermanager.models import Notification
from .models import Room, Message, TopicCount, Share
from .forms import PostForm, ShareForm
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

    shares = Share.objects.select_related('original', 'user') \
                          .order_by('-created')
    def timestamp(item):
        return getattr(item, 'created', item.updated)

    feed_items = sorted(chain(rooms, shares), key=timestamp,reverse=True)
    if request.user.is_authenticated:
        top_topics = ( TopicCount.objects.filter(user=request.user).order_by('-score').values_list('topic', flat=True)[:3])
        for_you_rooms = (Room.objects.filter(topic__in=top_topics).order_by('-updated')[:10])
    else:
        for_you_rooms = []

    return render(request, 'base/home.html', {
        'feed_items':    feed_items,
        'for_you_rooms': for_you_rooms,
    })

def room(request, pk):
   room = get_object_or_404(Room, pk=pk)
   if request.user.is_authenticated:
       affinity, _ = TopicCount.objects.get_or_create(
           user=request.user,
           topic=room.topic
       )
       affinity.score += 1
       affinity.save()
   comments = room.message_set.all().order_by('-created')
   if request.method == 'POST':
       comments = Message.objects.create(
           user=request.user,
           room=room,
           body=request.POST.get('body')
       )
       if room.host != request.user:
           Notification.objects.create(
               to_user=room.host,
               from_user=request.user,
               notif_type='post_comment',
               content_type=ContentType.objects.get_for_model(Message),
               object_id=comments.pk
           )
       return redirect('base:room', pk=room.id)
   context = {'room':room, 'comments':comments}
   return render(request, 'base/room.html', context)

@login_required(login_url='usermanager:user-login')
def postlike(request, pk):
    room = get_object_or_404(Room, pk=pk)
    liked_before = request.user in room.likes.all()

    if liked_before:
        room.likes.remove(request.user)
    else:
        room.likes.add(request.user)
        Notification.objects.create(
            to_user     = room.host,
            from_user   = request.user,
            notif_type  = 'post_like',
            content_type = ContentType.objects.get_for_model(Room),
            object_id    = room.pk
        )
    return redirect('base:room', pk=pk)


@login_required(login_url='usermanager:user-login')
def createpost(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
       form = PostForm(request.POST)
       if form.is_valid():
              room= form.save(commit=False)
              room.host= request.user
              room.save()
              return redirect('base:home')

    context={"form":form}
    return render(request, "base/room-form.html", context)

@login_required(login_url='usermanager:user-login')
def commentlike(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    liked_before = request.user in msg.likes.all()

    if liked_before:
        msg.likes.remove(request.user)
    else:
        msg.likes.add(request.user)
        Notification.objects.create(
            to_user     = msg.user,
            from_user   = request.user,
            notif_type  = 'comment_like',
            content_type = ContentType.objects.get_for_model(Message),
            object_id    = msg.pk
        )

    return redirect('base:room', pk=msg.room.pk)

@login_required(login_url='usermanager:user-login')
def updatepost(request, pk):
    room = Room.objects.get(id=pk)
    form = PostForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You can't do that")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=room)
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
def deleteshared(request, pk):
    sharedroom = Share.objects.get(id=pk)
    if request.user == Share.user or request.user.has_perm('base.delete_room'):
     if request.method == 'POST':
       sharedroom.delete()
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
    top_topics = (TopicCount.objects.filter(user=request.user).order_by("-score").values_list("topic", flat=True)[:3])
    rooms = (Room.objects .filter(topic__in=top_topics).order_by("-updated")[:50])
    return render(request, "base/home.html", {"rooms": rooms})


@login_required(login_url='usermanager:user-login')
def shareroom(request, pk):
    original = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = ShareForm(request.POST, request.FILES)
        if form.is_valid():
            share = form.save(commit=False)
            share.user= request.user
            share.original= original
            share.save()
           #notif
            Notification.objects.create(
                to_user=original.host,
                from_user=request.user,
                notif_type='post_share',
                content_type=ContentType.objects.get_for_model(Share),
                object_id=share.pk
            )
            return redirect('base:home')
    else:
        form = ShareForm()

    return render(request, 'base/room-share.html', { 'original':original,'form': form})


