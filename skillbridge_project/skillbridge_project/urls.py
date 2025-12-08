"""
URL configuration for skillbridge_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from main import views as main_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main app URLs
    path('', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    path('explore/', main_views.explore, name='explore'),
    path('testimonials/', main_views.testimonials, name='testimonials'),
    path('contact/', main_views.contact, name='contact'),
    path('faq/', main_views.faq, name='faq'),
    # Support legacy /main path: serve home at /main/ and redirect bare /main -> home
    path('main/', main_views.home, name='main'),
    path('main', RedirectView.as_view(pattern_name='home', permanent=False)),
    
    # User app URLs
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/setup/', user_views.profile_setup, name='profile_setup'),
    path('profile/<str:username>/', user_views.profile_detail, name='profile_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)