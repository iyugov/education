from django.shortcuts import render, redirect
from django.contrib.auth import logout, views as auth_views

from .forms import CustomAuthForm

from .entities.common.menus.main_menu import MAIN_MENU


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render_page(request, 'base.html', {'username': request.user.username})


def render_page(request, template_name, context):
    context['main_menu'] = MAIN_MENU
    return render(request, template_name, context)
