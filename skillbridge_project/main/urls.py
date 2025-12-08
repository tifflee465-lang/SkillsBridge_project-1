from django .urls import path
from . import views
app_name = 'main'
urlspatterns=[
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/',views.contact,name='contact'),
    path('explore/',views.explore, name='explore'),
    path('testimonials/',views.testimonials,name='testimonials'),
    path('faq/',views.faq, name='faq'),
]
    
