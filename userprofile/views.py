from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth import get_user_model, logout as auth_logout
from .forms import AccountSettingsForm, ProfileForm, CustomPasswordChangeForm, AccountDeleteForm
from .models import Profile

User = get_user_model()

@login_required
def profile_modal(request):
    """
    Renders a page (or partial) that includes the modal dialog
    with sidebar: Account Settings, Sessions, Danger Zone.
    """
    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Instantiate the forms for GET requests
    settings_form = AccountSettingsForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)
    password_form = CustomPasswordChangeForm(user=request.user)
    delete_form = AccountDeleteForm()

    context = {
        'settings_form': settings_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'delete_form': delete_form,
    }
    return render(request, 'profile/profile_modal.html', context)

@login_required
def update_account_settings(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        settings_form = AccountSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if settings_form.is_valid() and profile_form.is_valid():
            settings_form.save()
            profile_form.save()
            messages.success(request, 'Account settings updated.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('profile/profile_modal.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password was updated successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('profile/profile_modal.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        delete_form = AccountDeleteForm(request.POST)
        if delete_form.is_valid():
            password = delete_form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user:
                # Log out and delete the account
                request.user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('account_login')
            else:
                messages.error(request, 'Password is incorrect.')
    return redirect('profile/profile_modal.html')
