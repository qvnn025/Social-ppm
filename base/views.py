from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Message
from .forms import PostForm


def home(request):
    rooms= Room.objects.all()
    context={'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
   room=Room.objects.get(id=pk)
   comments = room.message_set.all().order_by('-created')
   if request.method == 'POST':
       message=Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
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

    if request.method == 'POST':
      room.delete()
      return redirect('base:home')

    return render(request, 'base/delete.html', {"obj":room})

@login_required(login_url='usermanager:user-login')
def deletecomment(request, pk):
    comment = Message.objects.get(id=pk)

    if request.method == 'POST':
      comment.delete()
      return redirect('base:home')

    return render(request, 'base/delete.html', {"obj":comment})


