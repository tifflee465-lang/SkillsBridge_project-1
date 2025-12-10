# main/forms.py
from django import forms

# main/apps.py
from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    # No need to import ContactMessage here
    # This method will run after Django is fully loaded
    def ready(self):
        # Import models here if needed
        pass
