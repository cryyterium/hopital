from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('objects/', views.objects, name='objects'),
    path('room/', views.room, name='room'),
    path('admin-page/', views.admin_page, name='admin'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-objects/', views.manage_objects, name='manage_objects'),
    path('stats/', views.stats, name='stats'),
    path("validate/<int:user_id>/", views.validate_email, name="validate_email"),
]