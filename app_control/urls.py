from django.urls import path

from app_control.forms import EmailForm, PasswordForm, UserForm
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('sign_in/', views.RegistrationWizard.as_view([EmailForm, PasswordForm, UserForm]), name='sign_in'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard')
]
