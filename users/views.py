from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from .forms import UserEmailPasswordForm, UserProfileForm
from recipes.models import Recipe, Review
from django.contrib.auth.decorators import login_required

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
        else:
            print("Form submission without email_password_form in POST data")
            form1 = UserEmailPasswordForm()
    else:
        form1 = UserEmailPasswordForm()

    return render(request, 'users/register_email_password.html', {"form1": form1})


def register_profile(request):
    if request.method == "POST":
        # Add debug print statement 
        print("Form submitted:", request.POST)
        print("Session data:", request.session.items())
        
        form2 = UserProfileForm(request.POST)
        if form2.is_valid():
            try:
                # Create the user with the data from both forms
                email = request.session.get('email')
                password = request.session.get('password')
                
                print(f"Retrieved from session - Email: {email}, Password: {'*' * len(password) if password else 'None'}")
                
                if not email or not password:
                    # Handle case where session data is missing
                    print("Missing session data, redirecting to first step")
                    return redirect('users:register_email_password')
                    
                user = form2.save(commit=False)
                user.email = email
                user.set_password(password)
                
                print(f"About to save user with username: {user.username}, email: {user.email}")
                
                user.save()
                
                print(f"User saved with ID: {user.id}")
                
                # Clean up session data
                if 'email' in request.session:
                    del request.session['email']
                if 'password' in request.session:
                    del request.session['password']
                
                auth_login(request, user)  # Log the user in after registration
                print(f"User logged in, redirecting to profile")
                return redirect('users:profile_view')  # Redirect to the profile view after successful registration
            except Exception as e:
                print(f"Error creating user: {e}")
                # Add error handling here as needed
                return render(request, 'users/register_profile.html', {
                    "form2": form2,
                    "error": f"Error creating account: {str(e)}"
                })
        else:
            print("Form errors:", form2.errors)
    else:
        # Check if we have the necessary session data
        if 'email' not in request.session or 'password' not in request.session:
            print("Session data missing on GET request")
            return redirect('users:register_email_password')
            
        form2 = UserProfileForm()

    return render(request, 'users/register_profile.html', {"form2": form2})



# def user_register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)  # Use auth_login to avoid conflict
#             return redirect('/')  # Redirect to home page
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'users/register.html', {"form": form})

# Login user
def user_login(request):  # Renamed function
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use auth_login to avoid conflict
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")  # Redirect to home page
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect("/")