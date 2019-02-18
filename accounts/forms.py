
from django import forms
from djangoproj.settings import base
from accounts.models import UserProfile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.files.images import get_image_dimensions
from accounts import countries


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid Email.')
    class Meta:
        model = UserProfile
        fields =(
            'username',
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            )



    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.city = self.cleaned_data['city']
        user.date_of_birth = self.cleaned_data['date_of_birth']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):
    password=None
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
        'class': 'form-control',
        'rows' : 5,
        }
    ))
    city = forms.CharField(required=False)
    country = forms.ChoiceField(required=False, choices=countries.COUNTRIES)
    gender = forms.ChoiceField(required=False, choices=(('M', 'M'),('F', 'F'),('U','Unspecified')))
    profession = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'city',
            'country',
            'profession',
            'description',

        )

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.city = self.cleaned_data['city']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.country = self.cleaned_data['country']
        user.profession = self.cleaned_data['profession']
        user.description = self.cleaned_data['description']

        if commit:
            user.save()

        return user


class EditAvatar(forms.ModelForm):
    avatar = forms.ImageField(required=False, help_text=u'File cannot exceed 500kB.\n Can Only upload .jpg, .gif, and .png')
    class Meta:
        model = UserProfile
        fields = ('avatar',)



    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png', 'jpg']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (500 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 500k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

    def save(self, commit=True):
        av = super(EditAvatar, self).save(commit=False)

        av.avatar = self.cleaned_data['avatar']

        if commit:
            av.save()

        return av
