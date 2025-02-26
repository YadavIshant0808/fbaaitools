# your_app/forms.py
from django import forms
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Password'
        })

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


User = get_user_model()

class AccountSettingsForm(forms.ModelForm):
    # This form updates basic user fields (e.g., name, username, email)
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'custom-input', 'placeholder': 'Email'}),
        }

class ProfileForm(forms.ModelForm):
    # This form updates additional profile fields.
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_picture']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'Nickname'}),
            # For the file upload, you can add your own classes.
            'profile_picture': forms.FileInput(attrs={'class': 'custom-input'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    # Inherit from Django's PasswordChangeForm but override widgets.
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Confirm New Password'}),
        strip=False,
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Current Password'}),
        strip=False,
    )

class AccountDeleteForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-input', 'placeholder': 'Confirm Your Password'}),
        label="Confirm Password"
    )

