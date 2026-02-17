from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('register/', views.registration, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vote/', views.voting, name='vote'),
    path('results/', views.results, name='results'),
    path('register-user/', views.register_user),
    path('login-user/', views.login_user),
    path('submit-vote/', views.submit_vote),
]
