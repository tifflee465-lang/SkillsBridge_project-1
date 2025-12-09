# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import UserProfile, Skill, Testimonial
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SkillSelectionForm, TestimonialForm
from django.contrib.auth import logout, authenticate, login
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Please complete your profile.')
            return redirect('profile_setup')
    else:
        form = UserRegisterForm()
    
    context = {'form': form, 'title': 'Register'}
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'title': 'My Profile',
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_setup(request):
    profile = request.user.userprofile
    
    if request.method == 'POST':
        form = SkillSelectionForm(request.POST)
        if form.is_valid():
            profile.skills_offered.set(form.cleaned_data['skills_offered'])
            profile.skills_needed.set(form.cleaned_data['skills_needed'])
            messages.success(request, 'Your skills have been updated!')
            return redirect('profile')
    else:
        initial_data = {
            'skills_offered': profile.skills_offered.all(),
            'skills_needed': profile.skills_needed.all(),
        }
        form = SkillSelectionForm(initial=initial_data)
    
    skills = Skill.objects.all()
    categories = Skill.CATEGORY_CHOICES
    
    context = {
        'title': 'Setup Your Skills',
        'form': form,
        'skills': skills,
        'categories': categories,
    }
    return render(request, 'users/profile_setup.html', context)

def profile_detail(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    
    # Find potential matches (people who need what this user offers)
    potential_matches = UserProfile.objects.filter(
        skills_needed__in=user_profile.skills_offered.all()
    ).exclude(user=request.user).distinct()[:5]
    
    context = {
        'title': f'{user_profile.user.username}\'s Profile',
        'user_profile': user_profile,
        'potential_matches': potential_matches,
    }
    return render(request, 'users/profile_detail.html', context)



def logoutUser(request):
    context ={}
    logout(request)
    return redirect('home')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = User.objects.get(username=username)
        except:
            print("User does not exists!")

        user = authenticate(request, username= username, password = password)

        if user is not None: 
            login(request, user)
            return redirect('promoProducts')
        else:
            print('Wrong Credentials!!')

    context ={}
    return render(request,'users/login_form.html',context)