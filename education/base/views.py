from django.shortcuts import render, redirect
from django.contrib.auth import logout, views as auth_views

from .forms import CustomAuthForm


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'base.html', {'username': request.user.username})
