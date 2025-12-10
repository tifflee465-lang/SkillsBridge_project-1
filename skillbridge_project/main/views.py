# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import FAQ, ContactMessage
from .forms import ContactForm
from users.models import Testimonial, UserProfile, Skill
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User 
from users.forms import TestimonialForm  # This is correct
# Add this import
# Comment out unused imports if they don't exist:
# from users.utils import create_chat_room, send_match_notification

def home(request):
    context = {
        'title': 'Home',
        'testimonials': Testimonial.objects.filter(approved=True)[:3]
    }
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html', {'title': 'About'})

def explore(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    
    profiles = UserProfile.objects.select_related('user').filter(available=True)
    
    if query:
        profiles = profiles.filter(
            Q(skills__name__icontains=query) |  # Changed from skills_offered
            Q(user__username__icontains=query) |
            Q(bio__icontains=query)
        ).distinct()
    
    if category:
        profiles = profiles.filter(skills__category=category).distinct()  # Simplified
    
    if location:
        profiles = profiles.filter(location__icontains=location)
    
    skills = Skill.objects.all()
    
    # Define categories directly since Skill.CATEGORY_CHOICES doesn't exist
    categories = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('language', 'Language'),
        ('business', 'Business'),
        ('music', 'Music'),
        ('art', 'Art'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    
    context = {
        'title': 'Explore',
        'profiles': profiles,
        'skills': skills,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'selected_location': location,
    }
    return render(request, 'main/explore.html', context)

def testimonials(request):
    """View testimonials"""
    testimonials_list = Testimonial.objects.filter(approved=True)
    
    # Only show form if user is authenticated
    if request.user.is_authenticated:
        from users.forms import TestimonialForm
        if request.method == 'POST':
            form = TestimonialForm(request.POST)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.user = request.user
                testimonial.author = request.user
                testimonial.save()
                messages.success(request, 'Your testimonial has been submitted for review!')
                return redirect('testimonials')
        else:
            form = TestimonialForm()
    else:
        form = None
    
    context = {
        'title': 'Success Stories',
        'testimonials': testimonials_list,
        'form': form,
    }
    return render(request, 'main/testimonials.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'title': 'Contact Us',
        'form': form,
    }
    return render(request, 'main/contact.html', context)

def faq(request):
    faqs = FAQ.objects.all()
    categories = set(faqs.values_list('category', flat=True))
    
    context = {
        'title': 'FAQ',
        'faqs': faqs,
        'categories': categories,
    }
    return render(request, 'main/faq.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def connect_with_user(request, username):
    """Connect with a user and create match notification"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    other_user = get_object_or_404(User, username=username)
    
    # Get user profiles
    try:
        user_profile = request.user.profile
        other_profile = other_user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('home')
    
    # Find matching skills (simplified version)
    user_skills = set(user_profile.skills.all())
    other_skills = set(other_profile.skills.all())
    
    common_skills = user_skills & other_skills
    
    if common_skills:
        skill = list(common_skills)[0]
        messages.success(request, f'✅ You and {other_user.username} both know {skill.name}!')
        
        # Check if chat room exists, create if not
        existing_chat = None
        for chat in request.user.chat_rooms.all():
            if other_user in chat.participants.all():
                existing_chat = chat
                break
        
        if existing_chat:
            return redirect('chat_room', room_id=existing_chat.id)
        else:
            # Create simple chat room
            from users.models import ChatRoom
            chat_room = ChatRoom.objects.create()
            chat_room.participants.add(request.user, other_user)
            return redirect('chat_room', room_id=chat_room.id)
    else:
        messages.warning(request, 'No common skills found.')
        return redirect('profile_detail', username=username)