# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm, EditProfileForm
from .models import UserProfile

class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = EditProfileForm
    model = UserProfile
    list_display = ['email', 'username', 'date_of_birth', 'gender', 'city', 'country', 'profession']

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.site_header = 'Administration Page'
