# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import FAQ, ContactMessage
from .forms import ContactForm
from users.models import Testimonial, UserProfile, Skill

def home(request):
    return render(request, 'main/home.html')
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
    
    # Already imported UserProfile and Skill at the top
    profiles = UserProfile.objects.select_related('user').filter(available=True)
    
    if query:
        profiles = profiles.filter(
            Q(skills_offered__name__icontains=query) |
            Q(skills_needed__name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(bio__icontains=query)
        ).distinct()
    
    if category:
        profiles = profiles.filter(
            Q(skills_offered__category=category) |
            Q(skills_needed__category=category)
        ).distinct()
    
    if location:
        profiles = profiles.filter(location__icontains=location)
    
    skills = Skill.objects.all()
    categories = Skill.CATEGORY_CHOICES
    
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
    testimonials = Testimonial.objects.filter(approved=True)
    
    if request.method == 'POST':
        from users.forms import TestimonialForm  # Import locally to avoid circular import
        form = TestimonialForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Your testimonial has been submitted for review!')
            return redirect('testimonials')
    else:
        from users.forms import TestimonialForm  # Import locally
        form = TestimonialForm()
    
    context = {
        'title': 'Success Stories',
        'testimonials': testimonials,
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