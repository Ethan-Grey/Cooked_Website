from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout

# Create your views here.
def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Use auth_login to avoid conflict
            return redirect('/')  # Redirect to home page
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {"form": form})

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