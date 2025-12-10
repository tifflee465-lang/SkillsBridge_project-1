from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import UserProfile, Skill, Notification, ChatRoom, Message

# Registration view
def register(request):
    """Register a new user"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'users/register.html', context)

# Login view
def loginUser(request):
    """Login user"""
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
    else:
        form = AuthenticationForm()
    
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'users/login.html', context)

# Logout view
@login_required
def logoutUser(request):
    """Logout user"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Profile setup view
@login_required
def profile_setup(request):
    """Profile setup view - simple placeholder"""
    messages.info(request, 'Profile setup functionality coming soon!')
    return redirect('profile')

# User's own profile
@login_required
def profile(request):
    """User profile view"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'title': 'My Profile',
        'profile': user_profile,
    }
    return render(request, 'users/profile.html', context)

# View other user's profile
@login_required
def profile_detail(request, username):
    """View another user's profile"""
    user = get_object_or_404(User, username=username)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'title': f'{user.username}\'s Profile',
        'profile_user': user,
        'profile': profile,
    }
    return render(request, 'users/profile_detail.html', context)

# Connect with user
@login_required
def connect_with_user(request, username):
    """Connect with another user"""
    user_to_connect = get_object_or_404(User, username=username)
    
    # Check if chat room already exists
    existing_chat = ChatRoom.objects.filter(participants=request.user).filter(participants=user_to_connect).first()
    
    if existing_chat:
        # Redirect to existing chat
        return redirect('chat_room', room_id=existing_chat.id)
    else:
        # Create new chat room
        chat_room = ChatRoom.objects.create()
        chat_room.participants.add(request.user, user_to_connect)
        
        messages.success(request, f'Connected with {user_to_connect.username}!')
        return redirect('chat_room', room_id=chat_room.id)

@login_required
def chat_rooms(request):
    """List all chat rooms for the user"""
    chat_rooms = request.user.chat_rooms.all().order_by('-updated_at')
    
    context = {
        'title': 'Messages',
        'chat_rooms': chat_rooms,
    }
    return render(request, 'users/chat_rooms.html', context)

@login_required
def chat_room(request, room_id):
    """Chat room detail view"""
    chat_room = get_object_or_404(ChatRoom, id=room_id, participants=request.user)
    messages_list = chat_room.messages.all()
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                chat_room=chat_room,
                sender=request.user,
                content=content
            )
            
            # Update chat room timestamp
            chat_room.save()
    
    context = {
        'title': 'Chat',
        'chat_room': chat_room,
        'messages': messages_list,
        'other_user': chat_room.participants.exclude(id=request.user.id).first(),
    }
    return render(request, 'users/chat_room.html', context)

@login_required
def notifications(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark as read when viewing
    unread_notifications = notifications.filter(read=False)
    unread_notifications.update(read=True)
    
    context = {
        'title': 'Notifications',
        'notifications': notifications,
    }
    return render(request, 'users/notifications.html', context)