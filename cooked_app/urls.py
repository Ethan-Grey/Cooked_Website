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
from users.views import login_cancelled, login_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('users/', include('users.urls')),
    # Keep allauth URLs first to handle OAuth callbacks
    path('accounts/', include('allauth.urls')),
    # Then our custom error handlers
    path('accounts/social/login/cancelled/', login_cancelled, name='socialaccount_login_cancelled'),
    path('accounts/social/login/error/', login_error, name='socialaccount_login_error'),
    path('accounts/3rdparty/signup/', views.home, name='socialaccount_signup'),  # Redirect signup to home
    path('', views.home, name='home'),
    path('about-us/', views.about_us),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
