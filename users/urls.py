from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.user_register, name='register_email_password'),
    path('register/profile/', views.user_profile, name='register_profile'),  # Keep this for the registration profile form
    path('profile/', views.profile_view, name='profile_view'),  # For displaying the user details and created recipes
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]