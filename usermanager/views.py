from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login , logout
from base import urls

User = get_user_model()

def loginview(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'Invalid username or password')

    context={'page':page} #review context
    return render(request, 'usermanager/user-login.html', context)

def logoutview(request):
    logout(request)
    return redirect('base:home')

def registeruser(request):
    page = 'register'
    context={'page':page}
    return render(request, 'usermanager/user-login.html', context)

def profilerender(request, username):
    user = get_object_or_404(User, username=username)
    rooms = user.posts.all()
    return render(request, "usermanager/user-profile.html", {
        "user-profile": user,
        "rooms": rooms,
    })





