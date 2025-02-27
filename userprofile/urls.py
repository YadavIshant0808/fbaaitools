from django.urls import path
from userprofile import views
from allauth.account.views import login, logout, signup

urlpatterns = [
    path('login/', login, name='account_login'),
    path('logout/', logout, name='account_logout'),
    path('register/', signup, name='account_signup'),
    path('profile/', views.profile_modal, name='profile_modal'),
    path('profile/update/', views.update_account_settings, name='update_account_settings'),
    path('profile/password-change/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path("google_login_by_token/", views.GoogleLoginByToken.as_view(), name="google_login_by_token"),
] 