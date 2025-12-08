# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('creative', 'Creative Arts'),
        ('academic', 'Academic'),
        ('trade', 'Trade Skills'),
        ('home', 'Home & Garden'),
        ('health', 'Health & Wellness'),
        ('business', 'Business'),
        ('language', 'Language'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Skills offered and needed
    skills_offered = models.ManyToManyField(Skill, related_name='offered_by', blank=True)
    skills_needed = models.ManyToManyField(Skill, related_name='needed_by', blank=True)
    
    # Availability
    available = models.BooleanField(default=True)
    
    # Rating (average of all feedbacks)
    rating = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class SkillExchange(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_exchanges')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_exchanges')
    skill_requested = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requested_in')
    skill_offered = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='offered_in')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.requester.username} ↔ {self.provider.username}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    skill_exchanged = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Testimonial by {self.user.username}"