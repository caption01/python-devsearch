from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    othe_skills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topSkills': top_skills,
        'otherSkills': othe_skills,
    }
    return render(request, 'users/user-profile.html', context)

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exsit')
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            """Create session by django"""
            login(request, user) 
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is incorrect')
    
    context = {
        'page': page
    }

    return render(request, 'users/login-register.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, 'username success logout')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occured during registration')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login-register.html', context)

login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)