from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeType
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import CreateRecipe

# Create your views here.
def recipe_category(request, category):
    # Get the recipe type (case-insensitive)
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    
    # Get all recipes for this category
    category_recipes = recipe_type.recipes.all()
    
    # Get all recipe types for the navbar dropdown
    recipe_types = RecipeType.objects.all()
    
    context = {
        'category': recipe_type,
        'category_recipes': category_recipes,
        'recipe_types': recipe_types
    }
    
    return render(request, 'recipes/category.html', context)



def recipe_detail(request, category, slug):
    # Get the recipe type
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    
    # Get the specific recipe
    recipe = get_object_or_404(Recipe, slug=slug, recipetype=recipe_type)
    
    # Get all recipe types for the navbar dropdown
    recipe_types = RecipeType.objects.all()
    
    context = {
        'recipe': recipe,
        'recipe_types': recipe_types
    }
    
    return render(request, 'recipes/recipe_detail.html', context)


def all_recipes(request):
    recipes = Recipe.objects.all()
    recipe_types = RecipeType.objects.all()
    
    context = {
        'recipes': recipes,
        'recipe_types': recipe_types,
        'title': 'All Recipes'
    }
    
    return render(request, 'recipes/all_recipes.html', context)



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