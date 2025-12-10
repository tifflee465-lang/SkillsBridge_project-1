from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ... your existing models ...

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('profile_created', 'Profile Created'),
        ('match_found', 'Match Found'),
        ('message_received', 'Message Received'),
        ('exchange_request', 'Exchange Request'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        participant_names = [user.username for user in self.participants.all()]
        return f"Chat between {', '.join(participant_names)}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."

class Skill(models.Model):
    CATEGORY_CHOICES = [  # ADD THIS
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('language', 'Language'),
        ('business', 'Business'),
        ('music', 'Music'),
        ('art', 'Art'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,  # Use the choices
        default='other'
    )
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.ManyToManyField(Skill, related_name='users', blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)  # ADD THIS
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # ADD THIS
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
class SkillExchange(models.Model):
    EXCHANGE_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_requested')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_provided')
    skill_offered = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='exchanges_offered')
    skill_requested = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='exchanges_requested')
    status = models.CharField(max_length=20, choices=EXCHANGE_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.requester.username} ↔ {self.provider.username}"
# users/models.py - CORRECT Testimonial model

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials_received')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='testimonials_given',
        null=True,
        blank=True
    )
    content = models.TextField()
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    approved = models.BooleanField(default=False)  # ADD THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.author:
            return f"Testimonial for {self.user.username} by {self.author.username}"
        return f"Testimonial for {self.user.username} (Anonymous)"