from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utility import search_profiles, paginate_profiles

# Create your views here.
def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }

    print(profiles)

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
            return redirect('account')
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

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        print('edit profile', request.POST)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added success')

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was added updated')

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)

def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted')

        return redirect('account')

    context = {
        'object': skill
    }
    return render(request, 'delete_template.html', context)