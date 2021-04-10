from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from tasks.models import Task
from .forms import SignInForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from tasks.forms import DisplayTaskForm

from datetime import datetime


# Create your views here.


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        form = SignInForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.warning(request,
                                 'Your account is inactive. ')
        else:
            messages.warning(request, 'Invalid login details given.')


    form = SignInForm()
    return render(request, 'sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin'))


def dashboard(request):
    if request.user.is_authenticated:
        form = DisplayTaskForm(request.POST)

        tasks = Task.objects.filter(user=request.user).filter(reminder_time__gte=datetime.now())

        return render(request, 'table.html', {'form': form, 'tasks': tasks})
    else:
        return HttpResponseRedirect(reverse('signin'))