from django.urls import path

from app_control.forms import ContactForm1, ContactForm2
from . import views

urlpatterns = [
    path('login/', views.RegistrationWizard.as_view([ContactForm1, ContactForm2]), name='login')
]
