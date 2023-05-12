from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'accounts/index.html')


def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, 'Login successful.')
            return redirect('/account/assets')
        else:
            # Return an 'invalid login' error message.
            if user is None:
                messages.error(request, 'User does not exist.')
            else:
                messages.error(request, 'Invalid login.')
            return redirect('/login')
    else:
        return render(request, 'login.html', {})


def user_assets_view(request):
    return render(request, 'accounts/u_assets.html')
