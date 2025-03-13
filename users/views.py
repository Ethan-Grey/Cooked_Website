from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from .forms import UserEmailPasswordForm, UserProfileForm
from recipes.models import Recipe
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
    
    # CHANGE: Filter recipes by the user object instead of username
    recipes = Recipe.objects.filter(madeby=user)
    
    return render(request, 'users/profile_view.html', {'user': user, 'recipes': recipes})

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
                # Save the email and password in the session to use in the next form
                request.session['email'] = email
                request.session['password'] = password
                return redirect('users:register_profile')  # Redirect to the second form
        else:
            form1 = UserEmailPasswordForm()

    else:
        form1 = UserEmailPasswordForm()

    return render(request, 'users/register_email_password.html', {"form1": form1})


def user_profile(request):
    if request.method == "POST":
        form2 = UserProfileForm(request.POST)
        if form2.is_valid():
            # Create the user with the data from both forms
            email = request.session['email']
            password = request.session['password']
            user = form2.save(commit=False)
            user.email = email
            user.set_password(password)
            user.save()
            auth_login(request, user)  # Log the user in after registration
            return redirect('users:profile_view')  # Redirect to the profile view after successful registration
    else:
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