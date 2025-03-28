from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.models import User
from .forms import UserEmailPasswordForm, UserProfileForm, CustomLoginForm
from recipes.models import Recipe, Review
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from allauth.socialaccount.models import SocialAccount
from django.views.decorators.http import require_http_methods

# Create your views here.


@login_required
def edit_profile_view(request):
    # No changes needed here
    if request.method == 'POST':
        # Handle form submission
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Update user information
        user = request.user
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Redirect to profile page after successful update
        return redirect('users:profile_view')
    else:
        # Display the edit form
        context = {
            'user': request.user,
        }
        return render(request, 'users/edit_profile.html', context)

def profile_view(request):
    user = request.user  # Get the current logged-in user
    
    # Filter recipes by the user object instead of username
    recipes = Recipe.objects.filter(madeby=user)
    
    # Get favorite recipes
    favorite_recipes = user.favorite_recipes.all()
    
    # Get user reviews
    user_reviews = Review.objects.filter(user=user).select_related('recipe')
    
    context = {
        'user': user, 
        'recipes': recipes,
        'favorite_recipes': favorite_recipes,
        'user_reviews': user_reviews
    }
    
    return render(request, 'users/profile_view.html', context)

# You have two user_profile functions - you may want to resolve this duplication
@login_required 
def user_profile(request):
    # Get the current user
    user = request.user
    
    # CHANGE: Fetch recipes by the user object using madeby field
    recipes = Recipe.objects.filter(madeby=user)
    
    context = {
        'user': user,
        'recipes': recipes,
    }
    
    return render(request, 'users/user_profile.html', context)



def user_register(request):
    if request.method == "POST":
        form1 = UserEmailPasswordForm(request.POST)
        if form1.is_valid():
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password1']
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'This email is already registered. Please use a different email or sign in.'
                    })
                messages.error(request, 'This email is already registered. Please use a different email or sign in.')
                return redirect('users:register_email_password')

            # Store data in session
            request.session['email'] = email
            request.session['password'] = password
            request.session.modified = True

            # Return success response for AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Great! Now let\'s complete your profile.'
                })

            return redirect('users:register_profile')
        else:
            # If it's an AJAX request, return form errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: errors[0] for field, errors in form1.errors.items()}
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                })
            
    else:
        form1 = UserEmailPasswordForm()

    return render(request, 'users/register_email_password.html', {"form1": form1})


def register_profile(request):
    if request.method == "POST":
        form2 = UserProfileForm(request.POST)
        if form2.is_valid():
            try:
                email = request.session.get('email')
                password = request.session.get('password')
                
                if not email or not password:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Session expired. Please start the registration process again.'
                        })
                    return redirect('users:register_email_password')
                
                # Store all user data in session
                user_data = {
                    'email': email,
                    'password': password,
                    'username': form2.cleaned_data['username'],
                    'first_name': form2.cleaned_data['first_name'],
                    'last_name': form2.cleaned_data['last_name']
                }
                request.session['user_data'] = user_data
                
                # Generate verification token
                token = default_token_generator.make_token(User(username=user_data['username']))
                uid = urlsafe_base64_encode(force_bytes(user_data['username']))
                
                verification_url = request.build_absolute_uri(
                    f'/users/verify-email/{uid}/{token}/'
                )
                
                # Send verification email
                subject = 'Verify your email address'
                message = render_to_string('users/email_verification.html', {
                    'user': {'first_name': user_data['first_name']},
                    'verification_url': verification_url,
                })
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user_data['email']],
                    fail_silently=False,
                )
                
                # Clean up sensitive session data
                if 'email' in request.session:
                    del request.session['email']
                if 'password' in request.session:
                    del request.session['password']
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': f'Registration complete! Please check your email and verify your account before logging in.'
                    })
                
                return render(request, 'users/registration_success.html', {
                    'email': user_data['email']
                })
                
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Error in registration process: {str(e)}'
                    })
                return render(request, 'users/register_profile.html', {
                    "form2": form2,
                    "error": f"Error in registration process: {str(e)}"
                })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: errors[0] for field, errors in form2.errors.items()}
                return JsonResponse({
                    'status': 'error',
                    'errors': errors
                })
    else:
        if 'email' not in request.session or 'password' not in request.session:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Session expired. Please start the registration process again.'
                })
            return redirect('users:register_email_password')
            
        form2 = UserProfileForm()

    return render(request, 'users/register_profile.html', {"form2": form2})

def verify_email(request, uidb64, token):
    try:
        username = force_str(urlsafe_base64_decode(uidb64))
        user_data = request.session.get('user_data')
        
        if not user_data or user_data['username'] != username:
            return render(request, 'users/email_verification_failed.html')
            
        # Create the user only after email verification
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Clean up session data
        if 'user_data' in request.session:
            del request.session['user_data']
            
        return render(request, 'users/email_verification_success.html')
        
    except Exception as e:
        print(f"Error in email verification: {e}")
        return render(request, 'users/email_verification_failed.html')

# Login user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redirect to next URL if provided, otherwise home
            next_url = request.POST.get('next', '/')
            return HttpResponseRedirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')
            # Get the previous page URL, fallback to home
            referer = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer)
            
    # If someone tries to access the login URL directly, redirect to home
    return redirect('/')

def user_logout(request):
    logout(request)
    return redirect("/")

def login_cancelled(request):
    return render(request, 'users/login_cancelled.html')

def login_error(request):
    return render(request, 'users/login_error.html')

@require_http_methods(["GET"])
def google_login_callback(request):
    error = request.GET.get('error')
    state = request.GET.get('state')
    
    # Prepare the error message and type
    error_data = {
        'error_type': 'unknown',
        'message': 'An error occurred while trying to log in with Google. Please try again.'
    }
    
    if error == 'access_denied':
        error_data = {
            'error_type': 'access_denied',
            'message': 'The login process was cancelled. You can try again when you\'re ready.'
        }
    
    # Check if this is an email conflict
    elif error and 'email' in request.GET:
        email = request.GET.get('email')
        try:
            # Check if user exists with this email
            user = User.objects.get(email=email)
            if not SocialAccount.objects.filter(user=user, provider='google').exists():
                error_data = {
                    'error_type': 'email_exists',
                    'message': f'This email ({email}) is already registered. Please sign in with your password or reset it.',
                    'email': email
                }
        except User.DoesNotExist:
            pass

    # Redirect to home with error parameters
    redirect_url = f'/?error={error_data["error_type"]}&message={error_data["message"]}'
    if 'email' in error_data:
        redirect_url += f'&email={error_data["email"]}'
    
    return redirect(redirect_url)