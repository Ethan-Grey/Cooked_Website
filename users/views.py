from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
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
        # Step 1: Handle the first form (Email and Password)
        if 'email_password_form' in request.POST:
            form1 = UserEmailPasswordForm(request.POST)
            if form1.is_valid():
                email = form1.cleaned_data['email']
                password = form1.cleaned_data['password1']
                
                print(f"Storing in session - Email: {email}, Password: {'*' * len(password)}")
                
                # Save the email and password in the session to use in the next form
                request.session['email'] = email
                request.session['password'] = password
                request.session.modified = True  # Make sure session is saved
                
                print("Session data stored, redirecting to profile registration")
                return redirect('users:register_profile')  # Redirect to the second form
            else:
                print("Form errors:", form1.errors)
                # Let the form handle the error display naturally
                # The error will be displayed using the errorlist class in the template
        else:
            print("Form submission without email_password_form in POST data")
            form1 = UserEmailPasswordForm()
    else:
        form1 = UserEmailPasswordForm()

    return render(request, 'users/register_email_password.html', {"form1": form1})


def register_profile(request):
    if request.method == "POST":
        print("Form submitted:", request.POST)
        print("Session data:", request.session.items())
        
        form2 = UserProfileForm(request.POST)
        if form2.is_valid():
            try:
                email = request.session.get('email')
                password = request.session.get('password')
                
                print(f"Retrieved from session - Email: {email}, Password: {'*' * len(password) if password else 'None'}")
                
                if not email or not password:
                    print("Missing session data, redirecting to first step")
                    return redirect('users:register_email_password')
                
                # Store all user data in session instead of creating the user
                user_data = {
                    'email': email,
                    'password': password,
                    'username': form2.cleaned_data['username'],
                    'first_name': form2.cleaned_data['first_name'],
                    'last_name': form2.cleaned_data['last_name']
                }
                request.session['user_data'] = user_data
                
                # Generate verification token
                token = default_token_generator.make_token(User(username=user_data['username']))  # Temporary user for token generation
                uid = urlsafe_base64_encode(force_bytes(user_data['username']))  # Use username as uid since user doesn't exist yet
                
                verification_url = request.build_absolute_uri(
                    f'/users/verify-email/{uid}/{token}/'
                )
                
                # Send verification email
                subject = 'Verify your email address'
                message = render_to_string('users/email_verification.html', {
                    'user': {'first_name': user_data['first_name']},  # Pass minimal user data for template
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
                
                return render(request, 'users/registration_success.html', {
                    'email': user_data['email']
                })
                
            except Exception as e:
                print(f"Error in registration process: {e}")
                return render(request, 'users/register_profile.html', {
                    "form2": form2,
                    "error": f"Error in registration process: {str(e)}"
                })
        else:
            print("Form errors:", form2.errors)
    else:
        if 'email' not in request.session or 'password' not in request.session:
            print("Session data missing on GET request")
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
def user_login(request):  # Renamed function
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                # User exists but hasn't verified their email
                return render(request, 'users/login.html', {
                    "form": form,
                    "error": "Please verify your email address before logging in. Check your inbox for the verification link."
                })
            auth_login(request, user)  # Use auth_login to avoid conflict
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")  # Redirect to home page
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect("/")