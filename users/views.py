from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from .forms import UserEmailPasswordForm, UserProfileForm
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # Handle form submission
        # Update user information
        # Redirect back to profile page
        return redirect('users:profile')
    else:
        # Display the edit form
        context = {
            'user': request.user,
        }
        return render(request, 'users/edit_profile.html', context)


def profile_view(request):
    user = request.user  # Get the current logged-in user
    recipes = Recipe.objects.filter(madeby=user)  # Filter recipes by the logged-in user
    return render(request, 'users/profile_view.html', {'user': user, 'recipes': recipes})


@login_required 
def user_profile(request):
    # Get the current user
    user = request.user
    
    # Fetch the user's details and their recipes
    recipes = Recipe.objects.filter(user=user)  # Assuming each recipe is linked to a user
    
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