# users/admin.py
from django.contrib import admin
from .models import Notification, ChatRoom, Message, Skill, UserProfile, SkillExchange, Testimonial

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'read', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('user__username', 'message')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'chat_room', 'timestamp', 'read')
    list_filter = ('read', 'timestamp')
    search_fields = ('content', 'sender__username')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    filter_horizontal = ('skills',)
    search_fields = ('user__username', 'bio', 'location')

@admin.register(SkillExchange)
class SkillExchangeAdmin(admin.ModelAdmin):
    list_display = ('requester', 'provider', 'skill_offered', 'skill_requested', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('content', 'user__username', 'author__username')





