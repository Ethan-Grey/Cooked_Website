from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeType
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .forms import CreateRecipe
from . import models
from django.db.models import Q

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

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    
    # Ensure only the recipe owner can edit it
    if recipe.madeby != request.user:
        messages.error(request, "You don't have permission to edit this recipe.")
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = CreateRecipe(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your recipe '{recipe.recipename}' has been updated successfully!")
            return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)
    else:
        form = CreateRecipe(instance=recipe)
    
    return render(request, 'recipes/edit_recipe.html', {
        'form': form,
        'recipe': recipe
    })

@login_required(login_url="/users/login/")
def delete_recipe(request, recipe_id):
    # Get the recipe or return 404
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Check if the current user is the recipe creator
    if recipe.madeby != request.user:
        messages.error(request, "You cannot delete a recipe that you didn't create.")
        return redirect('users:profile')
    
    # Delete the recipe immediately
    recipe_name = recipe.recipename
    recipe.delete()
    messages.success(request, f"'{recipe_name}' has been deleted successfully.")
    return redirect('users:profile_view')




def search(request):
    query = request.GET.get('q', '')
    recipe_types = RecipeType.objects.all()
    
    if query:
        # Search in recipe name, description, and ingredients
        results = Recipe.objects.filter(
            Q(recipename__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        ).distinct()
    else:
        results = Recipe.objects.none()
    
    context = {
        'query': query,
        'results': results,
        'recipe_types': recipe_types,
        'title': f'Search Results for "{query}"'
    }
    
    return render(request, 'recipes/search_results.html', context)