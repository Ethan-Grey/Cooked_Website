from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeType, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .forms import CreateRecipe, ReviewForm
from . import models
from django.db.models import Q, Avg
from django.http import JsonResponse

# Create your views here.

def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == "POST":
        # Check if user already has a review for this recipe
        existing_review = Review.objects.filter(recipe=recipe, user=request.user).first()
        
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            
            if existing_review:
                messages.success(request, "Your review has been updated successfully!")
            else:
                messages.success(request, "Your review has been added successfully!")
                
            return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)
        else:
            messages.error(request, "There was an error with your review. Please try again.")
    
    return redirect('recipes:detail', category=recipe.recipetype.recipetype, slug=recipe.slug)

def home(request):
    # Get the 4 most recent recipes with their average ratings
    recipes = Recipe.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-id')[:4]
    
    context = {
        'recipes': recipes
    }
    return render(request, 'home.html', context)

def recipe_category(request, category):
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    # Get recipes for this category with their average ratings
    category_recipes = Recipe.objects.filter(recipetype=recipe_type).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-id')
    
    context = {
        'category': recipe_type,
        'category_recipes': category_recipes
    }
    return render(request, 'recipes/category.html', context)

def recipe_detail(request, category, slug):
    recipe_type = get_object_or_404(RecipeType, recipetype__iexact=category)
    recipe = get_object_or_404(Recipe, slug=slug, recipetype=recipe_type)
    recipe_types = RecipeType.objects.all()
    form = ReviewForm()
    
    # Calculate average rating with proper rounding
    avg_rating = recipe.reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        avg_rating = round(avg_rating)
    else:
        avg_rating = 0
    
    context = {
        'recipe': recipe,
        'recipe_types': recipe_types,
        'form': form,
        'avg_rating': avg_rating
    }
    
    return render(request, 'recipes/recipe_detail.html', context)

def all_recipes(request):
    # Get all recipes with their average ratings
    recipes = Recipe.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-id')
    
    context = {
        'recipes': recipes
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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': "You cannot delete a recipe that you didn't create."
            })
        messages.error(request, "You cannot delete a recipe that you didn't create.")
        return redirect('users:profile_view')
    
    if request.method == "POST":
        # Recipe deletion
        recipe_name = recipe.recipename
        recipe.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"'{recipe_name}' has been deleted successfully."
            })
        
        messages.success(request, f"'{recipe_name}' has been deleted successfully.")
        return redirect('users:profile_view')
    
    # If it's a GET request and not AJAX, show the confirmation page
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': "Invalid request method."
        })
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})

def search(request):
    query = request.GET.get('q', '') # gets the search query
    recipe_types = RecipeType.objects.all() # gets all recipe objects and sets it to recipe_types
    
    if query: # if the search query exists
        results = Recipe.objects.filter(
            Q(recipename__icontains=query) | # this | means itll include the results from these aswell   # checks if the users search is in the recipe name
            Q(description__icontains=query) |   # checks if its in the description
            Q(ingredients__icontains=query)     # checks if its in the ingredients
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).distinct()
    else:
        results = Recipe.objects.none() # else incase there is no objects in the recipes. meaning nor ecipe is made
    
    context = { # dictionary
        'query': query, # stores the users search
        'results': results, # stores the filtered recipe objects
        'recipe_types': recipe_types,   # gives the recipe categories
        'title': f'Search Results for "{query}"'    # creates a title for the results
    }
    
    return render(request, 'recipes/search_results.html', context) # puts the context which is the dictionary in the search_results.html

@login_required
def add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user in recipe.favorites.all():
        # Already in favorites, do nothing
        messages.info(request, f"'{recipe.recipename}' is already in your favorites.")
    else:
        recipe.favorites.add(request.user)
        messages.success(request, f"'{recipe.recipename}' added to your favorites!")
    
    # Redirect back to the recipe detail page
    return redirect('recipes:detail', category=recipe.recipetype.recipetype.lower(), slug=recipe.slug)

@login_required
def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
        messages.success(request, f"'{recipe.recipename}' removed from your favorites.")
    else:
        # Not in favorites, do nothing
        messages.info(request, f"'{recipe.recipename}' is not in your favorites.")
    
    # Redirect back to the recipe detail page
    return redirect('recipes:detail', category=recipe.recipetype.recipetype.lower(), slug=recipe.slug)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Ensure only the review author can delete it
    if review.user != request.user:
        messages.error(request, "You don't have permission to delete this review.")
        return redirect('users:profile_view')
    
    if request.method == "POST":
        recipe = review.recipe
        review.delete()
        messages.success(request, "Your review has been deleted successfully!")
        return redirect('users:profile_view')
    
    return redirect('users:profile_view')

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated successfully!")
            return redirect('users:profile_view')
        else:
            messages.error(request, "There was an error updating your review. Please try again.")
            
    return redirect('users:profile_view')