from django.urls import path
from . import views


urlpatterns = [
    # The landing page URL (with the contact form included)
    path('', views.landing_index, name='home'),
    path('tools/', views.home, name='tools'),
    # path('tools/planner', views.planner, name='planner'),
    
    path('tools/codeoptimiser/', views.codeoptimiser, name='codeoptimiser'),
    path('tools/create_session/', views.create_session, name='create_session'),
    path('tools/load_session/<int:session_id>/', views.load_session, name='load_session'),
    
     path('tools/studyplanner/', views.studyplanner, name='studyplanner'),
    path('tools/create_study_session/', views.create_study_session, name='create_study_session'),
    path('tools/load_study_session/<int:session_id>/', views.load_study_session, name='load_study_session'),
    path('tools/download_study_plan/<int:session_id>/', views.download_study_plan, name='download_study_plan'),
    
    path('tools/tutor/', views.tutor_view, name='tutor'),
    path('tools/create_worksheet_session/', views.create_worksheet_session, name='create_worksheet_session'),
    path('tools/load_worksheet_session/<int:session_id>/', views.load_worksheet_session, name='load_worksheet_session'),
    path('tools/download_worksheet/<int:session_id>/', views.download_worksheet, name='download_worksheet'),
    
    path('terms/', views.terms_of_service, name='terms'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('cookies/', views.cookies_policy, name='cookies'),
    
    path('tools/research/', views.research_view, name='researcher'),
    path('tools/create_research_session/', views.create_research_session, name='create_research_session'),
    path('tools/load_research_session/<int:session_id>/', views.load_research_session, name='load_research_session'),
    path('tools/download_research/<int:session_id>/', views.download_research, name='download_research'),
]
 