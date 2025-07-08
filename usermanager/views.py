from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login , logout
from django.contrib.contenttypes.models import ContentType
from base.forms import PfpForm
from usermanager.models import UserRegistrationForm, FriendRequest, Notification, Profile

User = get_user_model()

def loginview(request):
    page = 'login'
    form=UserRegistrationForm()
    if request.method == 'POST':
        identifier= request.POST.get('identifier', '').strip()
        password= request.POST.get('password', '').strip()

        if '@' in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "No account with that email.")
                return render(request, 'usermanager/user-login.html', {'page': page})
        else:
            username = identifier
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if not user.email:
               return redirect('usermanager:email-prompt')
            return redirect('base:home')

        messages.error(request, "Invalid username, email, or password.")

    return render(request, 'usermanager/user-login.html', {'page': page, 'form': form})


@login_required(login_url='usermanager:user-login')
def emailprompt(request):
    if request.method == 'POST':
         email = request.POST.get('email','').strip().lower()
         if not email:
             messages.error(request, "Email can’t be blank.")
         elif User.objects.filter(email__iexact=email).exists():
             messages.error(request, "That email is already in use.")
         else:
             request.user.email = email
             request.user.save()
             return redirect('base:home')
    return render(request, 'usermanager/email-prompt.html')

def logoutview(request):
    logout(request)
    return redirect('base:home')

def registeruser(request):
    page = 'register'
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user = authenticate(request,username=user.username,password=form.cleaned_data['password1'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('base:home')


        messages.error(request, 'Error during registration: see below')
        print(form.errors)   # DEBUG

    return render(request, 'usermanager/user-login.html', {
        'page': page,
        'form': form,
    })

def profilerender(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    rooms        = profile_user.posts.all()

    is_owner = request.user.is_authenticated and request.user == profile_user


    fr_qs = FriendRequest.objects.filter(from_user=request.user,to_user=profile_user) \
        if request.user.is_authenticated and not is_owner else FriendRequest.objects.none()

    pending_request  = fr_qs.filter(status='pending').exists()
    is_following     = fr_qs.filter(status='accepted').exists()
    rejected_request = fr_qs.filter(status='rejected').exists()

    can_send_request = request.user.is_authenticated and not is_owner \
                       and not (pending_request or is_following)

    followers_count = FriendRequest.objects.filter(to_user=profile_user,status='accepted').count()

    return render(request, "usermanager/user-profile.html", {
        "profile_user":     profile_user,
        "rooms":            rooms,
        "followers_count":  followers_count,
        "can_send_request": can_send_request,
        "pending_request":  pending_request,
        "is_following":     is_following,
        "rejected_request": rejected_request,
    })

def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = PfpForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('usermanager:user-profile', pk=request.user.id)
    return render(request, 'usermanager/edit-profile.html', {'form': form})

@login_required(login_url='usermanager:user-login')
def sendreq(request, pk):
    to_user = get_object_or_404(User, pk=pk)

    if to_user == request.user:
        messages.error(request, "You can’t friend yourself.")
        return redirect('usermanager:user-profile', pk=pk)

    fr = FriendRequest.objects.filter(from_user=request.user,to_user=to_user).first()

    if fr is None:
        fr = FriendRequest.objects.create(from_user=request.user,to_user=to_user)
        Notification.objects.create(to_user=to_user,from_user=request.user,notif_type='friend_request')
        messages.success(request, "Friend request sent!")

    elif fr.status == 'rejected':
        fr.status = 'pending'
        fr.save()
        Notification.objects.create(to_user=to_user,from_user=request.user,notif_type='friend_request')
        messages.success(request, "Friend request sent!")

    elif fr.status == 'pending':
        #pending guard
        messages.info(request, "Your friend request is still pending.")

    elif fr.status == 'accepted':
        #accepted guard
        messages.info(request, "You’re already friends.")

    return redirect('usermanager:user-profile', pk=pk)

#notif inbox
@login_required(login_url='usermanager:user-login')
def notifbox(request):
    notifs = Notification.objects.filter(
        to_user=request.user,
        is_read=False
    )
    return render(request, 'usermanager/inbox.html', {
        'notifs': notifs
    })

@login_required(login_url='usermanager:user-login')
def respondreq(request, notif_id, action):
    notif = get_object_or_404(Notification,pk=notif_id,to_user=request.user,notif_type='friend_request',is_read=False)
    fr = get_object_or_404(
 FriendRequest,from_user=notif.from_user,to_user=request.user,status='pending')
    if action == 'accept':
        fr.accept()

        notif.is_read = True
        notif.save()
        Notification.objects.create(
            to_user=fr.from_user,
            from_user=request.user,
            notif_type='friend_accept',
            content_type=ContentType.objects.get_for_model(FriendRequest),
            object_id=fr.pk
        )
        Notification.objects.create(
            to_user=request.user,
            from_user=fr.from_user,
            notif_type='friend_accept',
            content_type=ContentType.objects.get_for_model(FriendRequest),
            object_id=fr.pk
        )
    elif action == 'reject':
        fr.reject()
        notif.is_read = True
        notif.save()
        messages.info(request, "Friend request rejected.")
    else:
        messages.error(request, "Unknown action.")

    return redirect('usermanager:inbox')


@login_required(login_url='usermanager:user-login')
@permission_required('usermanager.can_ban_user', raise_exception=True)
def ban(request, user_id):
    #admin exclusion
    target = get_object_or_404(User, pk=user_id)
    if target.is_superuser:
        messages.error(request, "Can't ban the admin.")
        return redirect('usermanager:user-profile', pk=user_id)

    #flag
    target.is_active = not target.is_active
    target.save()

    if not target.is_active:
        messages.success(request, f"{target.username} has been banned.")
    else:
        messages.success(request, f"{target.username} has been unbanned.")
    return redirect('usermanager:user-profile', pk=user_id)