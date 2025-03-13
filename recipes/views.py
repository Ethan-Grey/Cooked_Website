from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeType
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .forms import CreateRecipe
from . import models

# Create your views here.
def recipe_category(request, category):
    # No changes needed here
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    category_recipes = recipe_type.recipes.all()
    recipe_types = RecipeType.objects.all()
    
    context = {
        'category': recipe_type,
        'category_recipes': category_recipes,
        'recipe_types': recipe_types
    }
    
    return render(request, 'recipes/category.html', context)

def recipe_detail(request, category, slug):
    # No changes needed here
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    recipe = get_object_or_404(Recipe, slug=slug, recipetype=recipe_type)
    recipe_types = RecipeType.objects.all()
    
    context = {
        'recipe': recipe,
        'recipe_types': recipe_types
    }
    
    return render(request, 'recipes/recipe_detail.html', context)

def all_recipes(request):
    # No changes needed here
    recipes = Recipe.objects.all()
    recipe_types = RecipeType.objects.all()
    
    context = {
        'recipes': recipes,
        'recipe_types': recipe_types,
        'title': 'All Recipes'
    }
    
    return render(request, 'recipes/all_recipes.html', context)

@login_required(login_url="/users/login/")
def new_recipes(request):
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            
            # CHANGE: Simply assign the user object instead of name string
            recipe.madeby = request.user
                
            recipe.save()
            return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)
    else:
        form = CreateRecipe()
    
    return render(request, 'recipes/new_recipe.html', {'form': form})

@login_required(login_url="/users/login/")
def edit_recipe(request, pk):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    
    # CHANGE: Check if the current user owns this recipe using the ForeignKey
    if recipe.madeby != request.user:
        return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)
    
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)
    else:
        form = CreateRecipe(instance=recipe)
    
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def delete_recipe(request, recipe_id):
    # Get the recipe or return 404
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # CHANGE: Check using the ForeignKey (also fixed variable name from author to madeby)
    if recipe.madeby != request.user:
        messages.error(request, "You cannot delete a recipe that you didn't create.")
        return redirect('recipes:recipe_detail', recipe_id=recipe_id)
    
    # If it's a POST request, delete the recipe
    if request.method == 'POST':
        recipe_name = recipe.recipename  # Save the name for the success message (fixed variable name)
        recipe.delete()
        messages.success(request, f"'{recipe_name}' has been deleted successfully.")
        return redirect('recipes:user_recipes')  # Or wherever you want to redirect after deletion
    
    # If it's a GET request, show confirmation page
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})