from django.shortcuts import render, redirect
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    EditAvatar
    )
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages



class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = RegistrationForm()
        args = {'form':form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():

            #form.save()
            #return redirect('/djangoproj')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/confirm_email_page.html')

        form = RegistrationForm(request.POST)
        args = {'form':form}
        return render(request, 'accounts/register.html', args)

class Activate(TemplateView):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # return redirect('home')
            messages.success(request, f'Account Successfully Created!')
            return redirect('login')
        else:
            messages.error(request, f'Account activation failed... Try again later.')
            return redirect('register')

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/view_profile.html'

    def get(self, request):
        args = {'user': request.user}
        return render(request, self.template_name, args)

@method_decorator(login_required, name='dispatch')
class EditProfileView(TemplateView):
        template_name = 'accounts/edit_profile.html'

        def get(self, request):
            uform = EditProfileForm(instance=request.user)
            aform = EditAvatar(instance=request.user)
            args = {
                'uform':uform,
                'aform':aform

                }
            return render(request, self.template_name, args)


        def post(self, request):
            uform = EditProfileForm(request.POST, instance=request.user)
            aform = EditAvatar(request.POST, request.FILES, instance=request.user)

            if uform.is_valid() and aform.is_valid():
                uform.save()
                aform.save()
                messages.success(request, f'Profile Successfully Modified')
                return redirect('view_profile')

            uform = EditProfileForm(request.POST, instance=request.user)
            aform = EditAvatar(request.POST, request.FILES, instance=request.user)
            args = {
                'uform':uform,
                'aform':aform
                }

            return render(request, self.template_name, args)

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(TemplateView):
    template_name = 'accounts/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile/')
        form = PasswordChangeForm(data=request.POST, user=request.user)
        args = {'form': form}
        return render(request, self.template_name, args)

@method_decorator(login_required, name='dispatch')
class LoggedInView(TemplateView):
    template_name = 'accounts/loggedin.html'

    def get(self, request):
        return render(request, self.template_name)
