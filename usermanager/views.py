from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login , logout



from usermanager.models import UserRegistrationForm

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
            # if you need to prompt for missing email, do it here:
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

            user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data['password1']
            )
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
    rooms = profile_user.posts.all()
    return render(request, "usermanager/user-profile.html", {
        "profile_user": profile_user,
        "rooms": rooms,
    })






