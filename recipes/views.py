from django.shortcuts import render, redirect
from .models import Recipe, RecipeType
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import CreateRecipe

# Create your views here.
def breakfast(request):
    recipe_type = RecipeType.objects.get(recipetype="Breakfast")
    breakfast_recipes = recipe_type.recipes.all()
    return render(request, 'recipes/breakfast.html', {'breakfast_recipes': breakfast_recipes})


@login_required(login_url="/users/login/")
def new_recipes(request):
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            newrecipe = form.save(commit=False)
            newrecipe.save()
            return redirect("/")  # Redirect after saving

    else:
        form = CreateRecipe()  # Ensure GET requests return the form

    return render(request, 'recipes/new_recipes.html', {'form': form})  # Always return a response


