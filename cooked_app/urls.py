"""
URL configuration for cooked_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from users.views import login_cancelled, login_error, google_login_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls')),
    # Override allauth's login cancelled and error URLs
    path('accounts/3rdparty/login/cancelled/', login_cancelled, name='socialaccount_login_cancelled'),
    path('accounts/social/login/error/', login_error, name='socialaccount_login_error'),
    # Handle Google login callback errors
    path('accounts/google/login/callback/', google_login_callback, name='google_login_callback'),
    # Keep this after our overrides to allow other allauth URLs to work
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('about-us/', views.about_us),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
