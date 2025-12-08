from django.contrib import admin
from .models import Skill, UserProfile, SkillExchange, Testimonial

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'available', 'rating']
    list_filter = ['available', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    filter_horizontal = ['skills_offered', 'skills_needed']

@admin.register(SkillExchange)
class SkillExchangeAdmin(admin.ModelAdmin):
    list_display = ['requester', 'provider', 'skill_requested', 'skill_offered', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['requester__username', 'provider__username']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'skill_exchanged', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    search_fields = ['user__username', 'title', 'content']
    actions = ['approve_testimonials']
    
    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f'{queryset.count()} testimonials approved.')
    approve_testimonials.short_description = 'Approve selected testimonials'