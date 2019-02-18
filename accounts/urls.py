from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='view_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('change_password/',    ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/reset_password_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/reset_password_confirm.html'
    ), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/reset_password_complete.html'
    ), name='password_reset_complete'),
    path('loggedin/', LoggedInView.as_view(), name='loggedin'),
    path('register/activate/<str:uidb64>/<str:token>', Activate.as_view(), name='activate')
]
