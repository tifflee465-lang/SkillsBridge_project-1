from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Skill, Testimonial
# users/forms.py - create this file if it doesn't exist
from django import forms
from .models import Skill

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'phone', 'profile_picture', 'available']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class SkillSelectionForm(forms.Form):
    skills_offered = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    skills_needed = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )



class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['content', 'rating']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Share your experience...'
        })
        self.fields['rating'].widget = forms.Select(
            choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)],
            attrs={'class': 'form-control'}
        )
        self.fields['rating'].label = 'Rating (1-5 stars)'
        
       