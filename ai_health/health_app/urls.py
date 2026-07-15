from django.urls import path
from . import views

urlpatterns = [

    path("about/", views.about, name="about"),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.logout_view, name='logout'),

    path('health-monitor/', views.health_monitor, name='health_monitor'),

    path('history/', views.history, name='history'),

    path('tips/', views.tips, name='tips'),

    path("emergency/", views.emergency, name="emergency"),

    path("profile/", views.profile, name="profile"),

    path("download-report/", views.download_report, name="download_report"),
]