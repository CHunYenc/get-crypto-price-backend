from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#
import logging

# Create your views here.


def index(request):
    return render(request, 'accounts/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, 'Login successful.')
            logging.info(f"{username} login successful.")
            return redirect('/account/assets')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid login.')
            return redirect('/login')
    else:
        if request.user.is_authenticated:
            messages.info(request, '你已經登入過了喔！')
            return redirect('/account/assets')
        return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def user_assets_view(request):
    return render(request, 'accounts/u_assets.html')
