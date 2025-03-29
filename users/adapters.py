from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from allauth.account.models import EmailAddress

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True
        
    def get_signup_redirect_url(self, request):
        return settings.LOGIN_REDIRECT_URL
        
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if sociallogin.account.provider == 'google':
            base_username = data.get('email').split('@')[0]
            username = base_username
            User = get_user_model()
            
            # If username is taken, append a number (1, 2, 3, etc.)
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user.username = username
        return user
        
    def pre_social_login(self, request, sociallogin):
        # If email exists, connect the account to the existing user
        if sociallogin.email_addresses:
            email_address = sociallogin.email_addresses[0]
            User = get_user_model()
            try:
                user = User.objects.get(email=email_address.email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
        return super().pre_social_login(request, sociallogin)
        
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Now that the user is saved and has an ID, we can create the email address
        if sociallogin.account.provider == 'google':
            # Check if email already exists for this user
            EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={
                    'verified': True,
                    'primary': True
                }
            )
        return user

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return settings.LOGIN_REDIRECT_URL
        
    def get_login_redirect_url(self, request):
        return settings.LOGIN_REDIRECT_URL
        
    def is_open_for_signup(self, request):
        return True 