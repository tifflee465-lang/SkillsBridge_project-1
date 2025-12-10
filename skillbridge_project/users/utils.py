from .models import Notification

def create_notification(user, notification_type, message, link=None):
    """Create a notification for a user"""
    notification = Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        link=link
    )
    return notification

def send_profile_created_notification(user):
    """Send notification when profile is created"""
    message = "🎉 Congratulations! Your profile has been successfully created. Start exploring skills!"
    link = "/explore/"
    return create_notification(user, 'profile_created', message, link)

def send_match_notification(user, matched_user, skill):
    """Send notification when a match is found"""
    message = f"🤝 You have a match! {matched_user.username} needs {skill.name} which you offer."
    link = f"/profile/{matched_user.username}/"
    return create_notification(user, 'match_found', message, link)

def get_unread_notifications_count(user):
    """Get count of unread notifications"""
    return Notification.objects.filter(user=user, read=False).count()
def find_matches_for_user(user):
    """Find potential matches for a user based on skills"""
    user_profile = user.userprofile
    matches = []
    
    # Find users who need what this user offers
    for skill in user_profile.skills_offered.all():
        # Users who need this skill
        users_needing_skill = UserProfile.objects.filter(
            skills_needed=skill
        ).exclude(user=user)
        
        for match_profile in users_needing_skill:
            # Check if this user has skills the match offers
            common_skills = set(user_profile.skills_needed.all()) & set(match_profile.skills_offered.all())
            if common_skills:
                matches.append({
                    'profile': match_profile,
                    'skill_you_offer': skill,
                    'skill_they_offer': list(common_skills)[0],
                    'match_score': len(common_skills) * 10
                })
    
    return matches

def create_chat_room(user1, user2):
    """Create a chat room between two users"""
    from .models import ChatRoom
    
    # Check if chat room already exists
    existing_room = ChatRoom.objects.filter(
        participants=user1
    ).filter(
        participants=user2
    ).first()
    
    if existing_room:
        return existing_room
    
    # Create new chat room
    chat_room = ChatRoom.objects.create()
    chat_room.participants.add(user1, user2)
    
    # Create notification for both users
    create_notification(
        user1,
        'match_found',
        f"💬 Chat room created with {user2.username}! You can now message them.",
        f"/chat/{chat_room.id}/"
    )
    
    create_notification(
        user2,
        'match_found',
        f"💬 Chat room created with {user1.username}! You can now message them.",
        f"/chat/{chat_room.id}/"
    )
    
    return chat_room