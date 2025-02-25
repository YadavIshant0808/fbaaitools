from django.urls import path
from . import views

urlpatterns = [
    # The landing page URL (with the contact form included)
    path('', views.landing_index, name='home'),
    path('tools/', views.cookies_policy, name='tools'),
    path('tools/codeoptimiser', views.cookies_policy, name='optimiser'),
    path('tools/researcher', views.cookies_policy, name='researcher'),
    path('tools/planner', views.cookies_policy, name='planner'),
    path('tools/tutor', views.cookies_policy, name='tutor'),
    path('terms/', views.terms_of_service, name='terms'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('cookies/', views.cookies_policy, name='cookies'),
]
 