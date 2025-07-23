from django.urls import path
from accounts.views import auth, dashboard, profile
from django.contrib.auth import views as auth_views
from accounts.views.profile import custom_password_change_view

urlpatterns = [
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    path('profil/', profile.profile_view, name='profile'),
    path('profil/modifier/', profile.edit_profile_view, name='edit_profile'),
    path('dashboard/', dashboard.dashboard_view, name='dashboard'),
    path('password-change/', custom_password_change_view, name='password_change'),
    path('experience/ajouter/', profile.add_experience_view, name='add_experience'),
    path('experience/supprimer/<int:experience_id>/', profile.delete_experience_view, name='delete_experience'),
]
