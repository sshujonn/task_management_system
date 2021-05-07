from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from profiles.models import Profile
from tasks.models import Task
from .forms import SignInForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from helper.dboardutil import DBoardUtil, account_activation_token
from tasks.forms import DisplayTaskForm

from datetime import datetime

from profiles.service import ProfileService
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

            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            if user.is_active:
                profile = Profile.objects.get(pk=user.id)
                if profile.is_email_verified:
                    login(request, user)
                else:
                    messages.warning(request, 'Please activate your account. An email verification code was sent to your email.')
                    return render(request, 'sign_in.html', {'form': form})

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
        menu = ProfileService().get_menu(request.user)
        # import pdb;pdb.set_trace()
        return render(request, 'dashboard/dashboard.html', {'form': form, 'tasks': tasks, 'menu': menu})
    else:
        return HttpResponseRedirect(reverse('signin'))


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = form.cleaned_data.get('email')
            profile.save()

            DBoardUtil().sent_email(request, profile, 'Activate Your Task Manager Account.')

            return HttpResponseRedirect(reverse('signin'))
        else:
            # import pdb;pdb.set_trace()
            messages.warning(request, form.errors)
            # messages.warning(request, 'Your information is incorrect.')

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        profile = Profile.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        profile = None

    if profile is not None and account_activation_token.check_token(profile, token):
        profile.is_active = True
        profile.is_email_verified = True
        profile.save()
        login(request, profile)

        # messages.success(request,
        #                  'Thank you for your email confirmation. Now you can update your profile.')

        return HttpResponseRedirect(reverse('dashboard'))
        # return redirect('edit')
    else:
        return render(request, 'activation_code_invalid.html')